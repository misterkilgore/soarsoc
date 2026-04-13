import json
import firewall_manager

# Carica il file di log
with open('eve.json', 'r') as f:
    dati = json.load(f)

# Analizza ogni evento
for evento in dati:
    if evento.get("event_type") == "alert":
        # Se la severità è 1 (massima), blocca l'IP
        if evento["alert"]["severity"] == 1:
            ip_attaccante = evento["src_ip"]
            firewall_manager.blocca_ip(ip_attaccante)

# Mostra il risultato finale
print("\n--- STATO ATTUALE FIREWALL ---")
firewall_manager.mostra_bloccati()