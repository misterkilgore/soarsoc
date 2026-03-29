import sqlite3

def init_db():
    conn = sqlite3.connect('sicurezza.db')
    cursor = conn.cursor()
    
    # Creazione tabella
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utenti (
            username TEXT PRIMARY KEY,
            tentativi_falliti INTEGER DEFAULT 0,
            stato TEXT DEFAULT 'OK'
        )
    ''')
    
    # Dati di esempio
    utenti_demo = [
        ('admin', 0, 'OK'),
        ('mario_rossi', 2, 'OK'),
        ('luca_bianchi', 5, 'BLOCKED'),
        ('giovanna_verdi', 0, 'OK'),
        ('hacker_99', 12, 'BLOCKED'),
        ('staff_1', 1, 'OK'),
        ('guest', 0, 'OK'),
        ('locat_user', 3, 'BLOCKED'),
        ('robot_auto', 0, 'OK'),
        ('test_user', 0, 'OK')
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO utenti VALUES (?, ?, ?)', utenti_demo)
    
    conn.commit()
    conn.close()
    print("Database inizializzato con successo!")

if __name__ == "__main__":
    init_db()