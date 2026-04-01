from fastapi import FastAPI
import uvicorn
from procedure import aumenta_tentativi, blocca_utente, controlla_accessi, sblocca_accessi

app = FastAPI()

@app.post("/log/")
def check_login(username, esito):
    
    if esito == 'SUCCESS':
        sblocca_accessi(username)
    else:
        accessi = controlla_accessi(username)
        if accessi < 3:
            aumenta_tentativi(username)
        else:
            blocca_utente(username)
    
    
uvicorn.run(app, host="127.0.0.1", port=8000)