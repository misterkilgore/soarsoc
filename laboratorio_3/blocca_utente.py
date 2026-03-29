import sqlite3
import sys

if len(sys.argv) < 2:
    sys.exit(1)

user = sys.argv[1]
conn = sqlite3.connect('sicurezza.db')
cursor = conn.cursor()

cursor.execute("UPDATE utenti SET stato = 'BLOCKED' WHERE username = ?", (user,))
conn.commit()

if cursor.rowcount > 0:
    conn.close()
    sys.exit(0) # Successo
else:
    conn.close()
    sys.exit(1) # Utente non trovato