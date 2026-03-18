import pandas as pd
from datetime import datetime

alerts = pd.read_csv("alerts.csv")
columns = ["source_ip", "severity", "event_type", "description"]
tickets = alerts[columns]
tickets["status"] = "OPEN"

tecnici = {
"HIGH": "Giuseppe Neri",
"MEDIUM": "Giovanni Bianchi",
"LOW": "Mario Rossi"
}
tickets["assigned_to"] = tickets["severity"].map(tecnici)

now = datetime.now()
now.strftime("%Y-%m-%d %H:%M")
tickets["timestamp"] = now.strftime("%Y-%m-%d %H:%M")

tickets.to_csv("tickets.csv")
