import os

def blocca_ip(ip):
    """
    Blocca un IP aggiungendo una regola DROP in INPUT.
    """
    cmd = f"iptables -A INPUT -s {ip} -j DROP"
    os.system(cmd)
    print(f"[BLOCK] IP {ip} aggiunto alla blacklist del firewall.")

def sblocca_ip(ip):
    """
    Sblocca un IP rimuovendo la regola DROP specifica.
    """
    cmd = f"iptables -D INPUT -s {ip} -j DROP"
    os.system(cmd)
    print(f"[UNBLOCK] IP {ip} rimosso con successo.")

def mostra_bloccati():
    """
    Mostra gli IP attualmente bloccati (con regole DROP in INPUT).
    """
    print("IP bloccati nel firewall:")
    # Elenca regole INPUT e filtra quelle con DROP
    stream = os.popen("iptables -L INPUT -v -n --line-numbers")
    rules = stream.read().strip().split('\n')

    for line in rules:
        if "DROP" in line:
            # Estraggo IP sorgente dalla riga (solitamente la 8a colonna)
            parts = line.split()
            # Controllo che la riga abbia abbastanza colonne e che la colonna sorgente sia un IP
            if len(parts) >= 8:
                ip = parts
                print(f" - {ip}")

