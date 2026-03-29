import sqlite3
import sys

def aumenta_tentativi(username):
    try:
        # 1. Connessione al database
        conn = sqlite3.connect('sicurezza.db')
        cursor = conn.cursor()

        # 2. Incrementa il contatore di 1 per l'utente specificato
        cursor.execute("""
            UPDATE utenti 
            SET tentativi_falliti = tentativi_falliti + 1 
            WHERE username = ?
        """, (username,))

        # 3. Controllo se l'utente è stato trovato e salvataggio
        if cursor.rowcount > 0:
            conn.commit()
            
            # Recuperiamo il nuovo valore per dare un feedback all'utente
            cursor.execute("SELECT tentativi_falliti FROM utenti WHERE username = ?", (username,))
            nuovo_valore = cursor.fetchone()[0]
            
            print(f"❌ Incremento eseguito. Utente '{username}' ora ha {nuovo_valore} tentativi falliti.")
            conn.close()
            return 0
        else:
            print(f"⚠️ Errore: L'utente '{username}' non esiste.")
            conn.close()
            return 1

    except sqlite3.Error as e:
        print(f"💥 Errore database: {e}")
        return 1

if __name__ == "__main__":
    # Verifica l'argomento da linea di comando
    if len(sys.argv) < 2:
        print("Utilizzo: python aumenta_contatore.py <username>")
        sys.exit(1)

    user_input = sys.argv[1]
    esito = aumenta_tentativi(user_input)
    sys.exit(esito)