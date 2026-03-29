import sqlite3
import sys

if len(sys.argv) < 2:
    sys.exit(-1)

user = sys.argv[1]
conn = sqlite3.connect('sicurezza.db')
cursor = conn.cursor()

cursor.execute("SELECT tentativi_falliti FROM utenti WHERE username = ?", (user,))
result = cursor.fetchone()
conn.close()

if result:
    print(result[0])
    sys.exit(result[0])
else:
    sys.exit(0)