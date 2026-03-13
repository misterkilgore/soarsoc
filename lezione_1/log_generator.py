import json
import csv
import random
from datetime import datetime, timedelta

# Struttura Scenari per il Caseificio 4.0
scenarios_config = {
    "HIGH": {
        "probability": 0.10,  # 10% degli eventi
        "events": [
            "Industrial_Exploit_Attempt", "Ransomware_Lateral_Movement",
            "Unauthorized_PLC_Firmware_Update", "Exfiltration_Sensitive_Recipe",
            "VPN_Brute_Force_Success"
        ],
        "src": ["172.16.0.45", "192.168.20.15", "10.0.0.254"],
        "dst": ["192.168.10.50", "10.0.0.10", "192.168.10.101"]
    },
    "MEDIUM": {
        "probability": 0.30,  # 30% degli eventi
        "events": [
            "Multiple_Failed_Logins", "Abnormal_Data_Transfer",
            "New_DHCP_Server_Detected", "Unauthorized_IoT_Communication",
            "SQL_Injection_Attempt"
        ],
        "src": ["192.168.20.100", "192.168.20.20", "172.16.0.10"],
        "dst": ["52.143.45.110", "10.0.0.10", "192.168.20.200"]
    },
    "LOW": {
        "probability": 0.60,  # 60% degli eventi (Rumore)
        "events": [
            "Port_Scan_Internal", "ICMP_Flood_Small",
            "Printer_Offline_Alert", "DNS_Query_Anomaly",
            "NTP_Sync_Failure"
        ],
        "src": ["192.168.20.200", "192.168.10.101", "10.0.0.50"],
        "dst": ["8.8.8.8", "192.168.20.1", "10.0.0.254"]
    }
}

data_list = []
start_time = datetime(2026, 3, 12, 8, 0, 0)
levels = list(scenarios_config.keys())
weights = [scenarios_config[lvl]["probability"] for lvl in levels]

# Generazione dei 100 record
for i in range(100):
    # Sceglie la severità in base alla probabilità
    severity = random.choices(levels, weights=weights)[0]
    conf = scenarios_config[severity]

    timestamp = (start_time + timedelta(minutes=i*random.randint(1, 5))).isoformat() + "Z"

    record = {
        "timestamp": timestamp,
        "alert_id": f"ALT-{i+1:03d}",
        "source_ip": random.choice(conf["src"]),
        "destination_ip": random.choice(conf["dst"]),
        "severity": severity,
        "event_type": random.choice(conf["events"]),
        "description": f"Detected {severity} priority incident in MILKERS network"
    }
    data_list.append(record)

# Scrittura File (CSV, JSON, LOG)
# --- CSV ---
with open('alerts.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=data_list[0].keys())
    writer.writeheader()
    writer.writerows(data_list)

# --- JSON ---
with open('alerts.json', 'w') as f:
    json.dump(data_list, f, indent=2)

# --- LOG (Standard Syslog-like) ---
with open('alerts.log', 'w') as f:
    for r in data_list:
        f.write(f"{r['timestamp']} MILKERS-GW {r['event_type']}[{r['alert_id']}]: {r['severity']} - src={r['source_ip']} dst={r['destination_ip']}\n")

# --- YAML (Basic dump) ---
with open('alerts.yml', 'w') as f:
    f.write("alerts:\n")
    for r in data_list:
        f.write(f"  - id: {r['alert_id']}\n    type: {r['event_type']}\n    sev: {r['severity']}\n")

print(f"Creati 100 allarmi con distribuzione: {weights}")