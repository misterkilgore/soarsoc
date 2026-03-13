#!/bin/sh

cat << EOF
==============================================================
          SOC LAB: INCIDENT LOGGER - MILKERS Inc.
==============================================================

1. RECAP TOPOLOGIA DI RETE (MILKERS Inc.)
-----------------------------------------
L'infrastruttura simulata e' composta dalle seguenti zone:

- OT-Production (192.168.10.0/24):
  Asset critici: Silo-Control-Unit (.50), Temp-Sensor (.101).
- IT-Office (192.168.20.0/24):
  Asset: Workstation-Contabilita (.15), Printer (.200).
- Server-Farm (10.0.0.0/24):
  Asset: Logistics-DB (.10), Security-Gateway (.254).
- Cloud-Azure (52.143.45.110):
  Servizio: Gestionale ERP (MILK-ERP-Cloud).

I log vengono generati lanciando questo comando:



2. OBIETTIVO DELL'ESERCIZIO
---------------------------
Sviluppare uno script Python che:
1. Legga un file di alert in formato CSV.
2. Crei un file csv in cui ogni incidente viene assegnato ad un tecnico.

Eventualmente si possono sviluppare questi obiettivi avanzati:
1. Si connetta a un database SQLite locale.
2. Crei una tabella 'incidents' se non esiste.
3. Inserisca i dati del CSV nel database.
4. (Bonus) Provare a leggere le altre tipologie di file, oltre il csv.

3. DRITTE PYTHON: LIBRERIA PANDAS (Lettura CSV)
-----------------------------------------------
Per leggere i dati dal file CSV:

import pandas as pd

# Caricamento del file
df = pd.read_csv('alerts.csv')

# Accesso ai dati per riga
for index, row in df.iterrows():
    print(row['source_ip'], row['severity'])

4. DRITTE PYTHON: LIBRERIA SQLITE3 (Gestione DB)
------------------------------------------------
Per gestire il database SQL integrato:

import sqlite3

# Connessione (crea il file se non esiste)
conn = sqlite3.connect('milkers_soc.db')
cursor = conn.cursor()

# Creazione tabella
cursor.execute('''
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        source_ip TEXT,
        severity TEXT,
        description TEXT
    )
''')

# Inserimento dati (esempio)
cursor.execute("INSERT INTO incidents (source_ip, severity) VALUES (?, ?)", ('192.168.10.50', 'High'))
conn.commit()
conn.close()

==============================================================
EOF

