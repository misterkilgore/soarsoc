import sqlite3
import sys

if len(sys.argv) < 2:
    sys.exit(1)

user = sys.argv[1]
conn = sqlite3.connect('sicurezza.db')
cursor = conn.cursor()

# Sblocca e resetta i tentativi
cursor.execute("UPDATE utenti SET stato = 'OK', tentativi_falliti = 0 WHERE username = ?", (user,))
conn.commit()

if cursor.rowcount > 0:
    conn.close()
    sys.exit(0)
else:
    conn.close()
    sys.exit(1)