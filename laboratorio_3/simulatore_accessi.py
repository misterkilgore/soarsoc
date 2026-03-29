import sqlite3
import requests
import time
import random

# Configurazione
URL = "http://127.0.0.1:8000/log"
TIMEOUT_MIN = 1  # secondi
TIMEOUT_MAX = 5  # secondi

def get_random_user():
    conn = sqlite3.connect('sicurezza.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM utenti")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return random.choice(users) if users else None

def simulate_traffic():
    print("🚀 Simulatore di traffico avviato. Ctrl+C per fermare.")
    
    while True:
        user = get_random_user()
        if not user:
            print("Database vuoto!")
            break
            
        # 70% probabilità di fallimento per rendere il lab interessante
        esito = random.choices(["SUCCESS", "FAILED"], weights=[30, 70])[0]
        
        payload = {
            "username": user,
            "esito": esito
        }
        
        try:
            response = requests.post(URL, json=payload)
            print(f"[LOG] Utente: {user:15} | Esito: {esito:8} | Status Server: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("❌ Errore: Il server FastAPI non è raggiungibile!")

        # Aspetta un intervallo casuale
        wait_time = random.uniform(TIMEOUT_MIN, TIMEOUT_MAX)
        time.sleep(wait_time)

if __name__ == "__main__":
    simulate_traffic()