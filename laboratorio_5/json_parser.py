import json

# 1. Carichiamo il file simulato
with open('eve.json', 'r') as file:
    log_data = json.load(file)

# 2. Iteriamo attraverso ogni evento della lista
for event in log_data:
    
    # 3. Filtriamo solo gli eventi di tipo 'alert'
    if event.get("event_type") == "alert":
        ip_sorgente = event.get("src_ip")
        severita = event["alert"].get("severity")
        minaccia = event["alert"].get("signature")

        # 4. Logica di decisione
        if severita == 1:
            print(f"⚠️ ALLERTA CRITICA da {ip_sorgente}!")
            print(f"Attacco rilevato: {minaccia}")
            # Qui andrebbe il comando per iptables
        else:
            print(f"ℹ️ Alert minore da {ip_sorgente} (Severità: {severita})")