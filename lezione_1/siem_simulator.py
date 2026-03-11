#!/usr/bin/env python3
"""
SIMULATORE SIEM - Milkers INC.
Genera un flusso in tempo reale di eventi di sicurezza per il caseificio.
"""

import csv
import time
import random
import datetime
import sys
from typing import Dict, List, Tuple

# ============================================================
# CONFIGURAZIONE
# ============================================================

# Nome del file CSV di output
OUTPUT_FILE = "siem_logs_milkers.csv"

# Intervallo base tra un evento e l'altro (in secondi)
# Puoi modificarlo per simulare traffico più o meno intenso
BASE_DELAY = 2  # 2 secondi

# Variazione casuale del delay (+/- MAX_VARIATION)
# Esempio: con BASE_DELAY=2 e VARIATION=1, aspetta tra 1 e 3 secondi
VARIATION = 1

# ============================================================
# DATI DI SIMULAZIONE
# ============================================================

# Asset della rete (cosa abbiamo nell'infrastruttura)
ASSETS = {
    # IP, Nome, Ruolo, Criticità
    "192.168.1.10": ("ERP-Gestionale", "Server", "ALTA"),
    "192.168.1.20": ("NAS-Formaggi", "Server File", "ALTA"),
    "192.168.1.50": ("PC-Mario", "PC Impiegato", "MEDIA"),
    "192.168.1.51": ("PC-Giuseppe", "PC Impiegato", "MEDIA"),
    "192.168.1.100": ("Stampante-Ufficio", "Printer", "BASSA"),
    "192.168.2.10": ("WiFi-Ospite-1", "Client Ospite", "BASSA"),
    "192.168.2.11": ("WiFi-Ospite-2", "Client Ospite", "BASSA"),
    "10.10.10.5": ("Sensore-Temperatura-1", "Sensore IoT", "MEDIA"),
    "10.10.10.6": ("Sensore-Temperatura-2", "Sensore IoT", "MEDIA"),
    "10.10.10.50": ("Centralina-Mungitura", "Controller OT", "ALTA"),
    "10.10.10.100": ("Telecamera-Produzione", "Camera IP", "BASSA"),
    "172.16.1.10": ("WebServer-WordPress", "Web Server", "MEDIA"),
    "172.16.1.20": ("MailServer", "Mail Server", "MEDIA"),
    "192.168.1.254": ("Firewall-pfSense", "Firewall", "CRITICA"),
}

# Lista di utenti/ruoli per gli eventi
USERS = ["mario.rossi", "giuseppe.verdi", "admin", "produzione", "ospite", "sconosciuto"]

# Tipi di evento con relativi livelli di severità
EVENT_TEMPLATES = [
    # EVENTI NORMALI (green/blue team)
    {"action": "LOGIN_SUCCESS", "severity": "INFO", 
     "message": "Login riuscito - Utente: {user} da IP: {src}"},
    {"action": "LOGOUT", "severity": "INFO", 
     "message": "Logout utente {user}"},
    {"action": "FILE_ACCESS", "severity": "INFO", 
     "message": "Accesso file {file} su {dst} da {src}"},
    {"action": "BACKUP_COMPLETED", "severity": "INFO", 
     "message": "Backup giornaliero completato con successo"},
    {"action": "CONFIG_CHANGE", "severity": "WARNING", 
     "message": "Modifica configurazione su {dst} da {src}"},
    {"action": "SENSOR_DATA", "severity": "INFO", 
     "message": "Sensore {src}: Temperatura {temp}°C - Umidità {hum}%"},
    
    # ALLARMI (red team)
    {"action": "LOGIN_FAILED", "severity": "WARNING", 
     "message": "Tentativo di login fallito per {user} da IP: {src} - {count} tentativi"},
    {"action": "BRUTE_FORCE", "severity": "HIGH", 
     "message": "POSSIBILE BRUTE FORCE: {count} login falliti in {time} secondi da {src} verso {dst}"},
    {"action": "SQL_INJECTION", "severity": "CRITICAL", 
     "message": "Tentativo SQL Injection rilevato su {dst} - Payload: {payload}"},
    {"action": "PORTS_SCAN", "severity": "MEDIUM", 
     "message": "Port scan rilevato da {src} - {count} porte in {time}s"},
    {"action": "PHISHING_DETECTED", "severity": "HIGH", 
     "message": "Email sospetta rilevata - Mittente: {sender}, Oggetto: {subject}"},
    {"action": "SENSOR_ALERT", "severity": "HIGH", 
     "message": "ALLARME SENSORE {src}: Temperatura fuori range! Valore: {temp}°C (range: {min}-{max}°C)"},
    {"action": "UNAUTHORIZED_ACCESS", "severity": "CRITICAL", 
     "message": "Tentativo accesso non autorizzato a {dst} da {src}"},
    {"action": "MALWARE_DETECTED", "severity": "CRITICAL", 
     "message": "Malware rilevato su {dst} - {malware} - Azione: {action_taken}"},
    {"action": "VPN_CONNECTION", "severity": "INFO", 
     "message": "Connessione VPN stabilita da {src} verso {dst}"},
    {"action": "FIREWALL_BLOCK", "severity": "MEDIUM", 
     "message": "Firewall: Bloccato traffico da {src}:{sport} a {dst}:{dport} - {protocol}"},
]

# File casuali per accessi
FILES = ["ordini_2026.csv", "ricetta_parmigiano.pdf", "bilancio_Q1.xlsx", 
         "produzione_giornaliera.log", "clienti_privati.xlsx", "config_mungitrice.ini"]

# Payload SQL per attacchi
SQL_PAYLOADS = ["' OR '1'='1", "'; DROP TABLE users; --", "' UNION SELECT * FROM passwords--", 
                "admin'--", "../etc/passwd", "<script>alert(1)</script>"]

# Email di phishing
PHISHING_EMAILS = [
    ("noreply@paypal-update.com", "Il tuo account è stato sospeso"),
    ("amazon-alerts@secure-verify.net", "Problema con il tuo ordine #12345"),
    ("hr@milkers-inc.local", "URGENTE: Modifica contratto lavoro"),
    ("dirigenza@milkers-inc.local", "Nuove policy aziendali - clicca per accettare")
]

# Malware
MALWARE = ["Ransomware", "Keylogger", "Trojan", "Backdoor", "CryptoMiner"]

# ============================================================
# FUNZIONI DI GENERAZIONE
# ============================================================

def get_random_ip(zone_filter=None):
    """Restituisce un IP casuale dalla lista, opzionalmente filtrato per zona"""
    ips = list(ASSETS.keys())
    if zone_filter:
        # Filtra per subnet (es. '192.168.1' per LAN)
        ips = [ip for ip in ips if ip.startswith(zone_filter)]
    return random.choice(ips) if ips else "0.0.0.0"

def get_random_external_ip():
    """Simula un IP esterno (Internet)"""
    return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def generate_event(timestamp):
    """Genera un singolo evento casuale"""
    
    # Scegli un template di evento
    template = random.choice(EVENT_TEMPLATES)
    
    # Seleziona IP sorgente e destinazione in base al tipo di evento
    if random.random() < 0.3:  # 30% di probabilità che sia un IP esterno
        src_ip = get_random_external_ip()
    else:
        src_ip = get_random_ip()
    
    # La destinazione è di solito un asset interno
    dst_ip = get_random_ip()
    
    # Evita che src e dst siano uguali (a meno che non sia voluto)
    if src_ip == dst_ip and src_ip != "0.0.0.0":
        dst_ip = get_random_ip()
        while dst_ip == src_ip:
            dst_ip = get_random_ip()
    
    # Costruisci i campi variabili del messaggio
    fields = {
        "user": random.choice(USERS),
        "src": src_ip,
        "dst": dst_ip,
        "sport": random.randint(1024, 65535),
        "dport": random.choice([22, 80, 443, 3306, 5432, 8080, 21]),
        "protocol": random.choice(["TCP", "UDP", "ICMP"]),
        "file": random.choice(FILES),
        "count": random.randint(5, 100),
        "time": random.randint(10, 300),
        "temp": round(random.uniform(2.0, 8.0), 1) if random.random() < 0.5 else round(random.uniform(15.0, 25.0), 1),
        "hum": random.randint(40, 80),
        "min": 4.0,
        "max": 6.0,
        "payload": random.choice(SQL_PAYLOADS),
        "sender": random.choice(PHISHING_EMAILS)[0],
        "subject": random.choice(PHISHING_EMAILS)[1],
        "malware": random.choice(MALWARE),
        "action_taken": random.choice(["Bloccato", "Messo in quarantena", "Rimosso"]),
    }
    
    # Costruisci il messaggio completo
    message = template["message"].format(**fields)
    
    # Costruisci l'evento completo
    event = {
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "src_ip": fields["src"],
        "dst_ip": fields["dst"],
        "src_name": ASSETS.get(fields["src"], ("Sconosciuto", "", ""))[0] if fields["src"] in ASSETS else "Esterno",
        "dst_name": ASSETS.get(fields["dst"], ("Sconosciuto", "", ""))[0] if fields["dst"] in ASSETS else "Esterno",
        "action": template["action"],
        "severity": template["severity"],
        "message": message,
        "user": fields["user"],
        "protocol": fields["protocol"],
        "sport": fields["sport"],
        "dport": fields["dport"],
    }
    
    return event

def write_csv_header():
    """Scrive l'intestazione del file CSV"""
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'timestamp', 'src_ip', 'dst_ip', 'src_name', 'dst_name',
            'action', 'severity', 'message', 'user', 'protocol', 'sport', 'dport'
        ])
        writer.writeheader()

def append_to_csv(event):
    """Aggiunge un evento al file CSV"""
    with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=event.keys())
        writer.writerow(event)

def print_event(event):
    """Stampa l'evento a schermo con colorazione in base alla severità"""
    severity_colors = {
        "INFO": "\033[92m",      # Verde
        "WARNING": "\033[93m",    # Giallo
        "MEDIUM": "\033[93m",     # Giallo
        "HIGH": "\033[91m",       # Rosso
        "CRITICAL": "\033[91m\033[1m",  # Rosso grassetto
    }
    reset = "\033[0m"
    
    color = severity_colors.get(event['severity'], "\033[0m")
    
    print(f"{color}[{event['timestamp']}] [{event['severity']:^8}] {event['action']:20} - {event['message']}{reset}")
    print(f"      Fonte: {event['src_name']} ({event['src_ip']}) -> Dest: {event['dst_name']} ({event['dst_ip']})")
    print("-" * 100)

# ============================================================
# MAIN LOOP
# ============================================================

def main():
    print("\n" + "="*60)
    print(" 🧀  MILKERS INC. - SIEM SIMULATOR  🧀")
    print("="*60)
    print(f"\nGenerazione log in {OUTPUT_FILE}")
    print(f"Delay base: {BASE_DELAY}s ± {VARIATION}s")
    print("\nPremi Ctrl+C per terminare\n")
    print("-"*100)
    
    # Inizializza il file CSV
    write_csv_header()
    
    try:
        while True:
            # Genera timestamp corrente
            now = datetime.datetime.now()
            
            # Genera evento
            event = generate_event(now)
            
            # Salva su CSV
            append_to_csv(event)
            
            # Stampa a schermo
            print_event(event)
            
            # Calcola il prossimo delay
            delay = BASE_DELAY + random.uniform(-VARIATION, VARIATION)
            delay = max(0.1, delay)  # Non meno di 0.1 secondi
            
            time.sleep(delay)
            
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print(" Simulazione terminata. Arrivederci!")
        print(f" Log salvati in: {OUTPUT_FILE}")
        print("="*60)

if __name__ == "__main__":
    main()