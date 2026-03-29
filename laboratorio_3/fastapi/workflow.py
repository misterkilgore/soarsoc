from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from datetime import datetime, timedelta
from typing import Dict

app = FastAPI()

# IP blacklist (esempio statico)
blacklist = {"203.0.113.1"}

# Stato tentativi falliti per IP e account
failed_attempts: Dict[str, int] = {}

# Stato blocco account per IP
blocked_accounts: Dict[str, datetime] = {}

# Costanti
MAX_FAILED_ATTEMPTS = 5
BLOCK_TIME = timedelta(minutes=15)

def is_ip_blacklisted(ip: str) -> bool:
    return ip in blacklist

def log_event(ip: str, success: bool):
    timestamp = datetime.utcnow().isoformat()
    print(f"{timestamp} - Login {'success' if success else 'failure'} from IP {ip}")

def send_notification(ip: str):
    # In un sistema reale invieresti email o alert
    print(f"NOTIFICA: Tentativi sospetti da IP {ip}")

@app.get("/login", response_class=PlainTextResponse)
async def handle_login(ip: str, success: str):
    ip = ip.strip()
    success = success.lower() == "true"
    
    # Azione comune: controllo blacklist
    if is_ip_blacklisted(ip):
        return "Accesso negato: IP in blacklist"
    
    # Controlla se account è bloccato
    if ip in blocked_accounts:
        unblock_time = blocked_accounts[ip]
        if datetime.utcnow() < unblock_time:
            return f"Account bloccato fino a {unblock_time.isoformat()}"
        else:
            del blocked_accounts[ip]
            failed_attempts[ip] = 0  # reset contatore
    
    if success:
        # Login riuscito
        failed_attempts[ip] = 0  # reset contatore tentativi falliti
        log_event(ip, True)
        return "Login riuscito"
    
    else:
        # Login fallito
        failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
        log_event(ip, False)
        
        if failed_attempts[ip] > MAX_FAILED_ATTEMPTS:
            # Blocca account e invia notifica
            blocked_accounts[ip] = datetime.utcnow() + BLOCK_TIME
            send_notification(ip)
            return f"Account bloccato per tentativi falliti da IP {ip}"
        else:
            # Delay progressivo
            delay_seconds = failed_attempts[ip]
            import time
            time.sleep(delay_seconds)
            return f"Login fallito. Ritenta tra {delay_seconds} secondi."

