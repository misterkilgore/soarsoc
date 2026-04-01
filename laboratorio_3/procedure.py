import sqlite3
import sys

def aumenta_tentativi(user):

    conn = sqlite3.connect('sicurezza.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE utenti 
        SET tentativi_falliti = tentativi_falliti + 1 
        WHERE username = ?
    """, (user,))

    if cursor.rowcount > 0:
        conn.commit()
        cursor.execute("SELECT tentativi_falliti FROM utenti WHERE username = ?", (user,))
        nuovo_valore = cursor.fetchone()[0]            
        print(f"⚠️ Incremento eseguito. Utente '{user}' ora ha {nuovo_valore} tentativi falliti.")
        conn.close()
        return 0
    else:
        print(f"⚠️ Errore: L'utente '{user}' non esiste.")
        conn.close()
        return 1

def blocca_utente(user):
    conn = sqlite3.connect('sicurezza.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE utenti SET stato = 'BLOCKED' WHERE username = ?", (user,))
    conn.commit()

    if cursor.rowcount > 0:
        print(f"❌ L'utente '{user}' è stato bloccato.")
        conn.close()
        return 0
    else:
        conn.close()
        return 1

def controlla_accessi(user):
    conn = sqlite3.connect('sicurezza.db')
    cursor = conn.cursor()

    cursor.execute("SELECT tentativi_falliti FROM utenti WHERE username = ?", (user,))
    result = cursor.fetchone()
    conn.close()

    if result:
        print(f"⚠️ L'utente '{user}' ha {result[0]} tentativi falliti.")
        return result[0]
    else:
        return 0

def sblocca_accessi(user):
    conn = sqlite3.connect('sicurezza.db')
    cursor = conn.cursor()

    # Sblocca e resetta i tentativi
    cursor.execute("UPDATE utenti SET stato = 'OK', tentativi_falliti = 0 WHERE username = ?", (user,))
    conn.commit()

    if cursor.rowcount > 0:
        print(f"✅ L'utente '{user}' è stato sbloccato.")
        conn.close()
        return 0
    else:
        conn.close()
        return 1