# SOC/SOAR Course - Lab Repository

Questa repository raccoglie il materiale pratico, gli script e i file di configurazione sviluppati durante il corso **SOC/SOAR**. 

L'obiettivo del progetto è simulare le attività di un analista di sicurezza all'interno di un ambiente industriale (Caseificio 4.0 - MILKERS Inc.), automatizzando la gestione degli incidenti tramite Python.

## Struttura del Corso

In questa sezione verranno aggiunte progressivamente le descrizioni e gli obiettivi di ogni lezione.

### Laboratorio 1: Log Management e Ticketing Base
* **Obiettivo**: Simulare la ricezione di alert e il loro salvataggio strutturato.
* **Descrizione**: 
    - Analisi preliminare dei log in formato CSV tramite la libreria `pandas`.
    - Normalizzazione dei dati e gestione della priorità (triage).
    - Assegnazione automatica dei ticket ai tecnici in base alla severità degli alert.
	
### Laboratorio 2: Dashboarding
* **Obiettivo**: Simulare la creazione di una dashboard per la gestione di un SOC.
* **Descrizione**: 
    - Installazione di una dashboard remota utilizzando `streamlit`.
	- Visualizzazione di tickets e metriche.
	- Modifica dello stato di lavorazione dei ticket.
	
### Laboratorio 3: Workflow e FastAPI
* **Obiettivo**: Simulare un workflow di risposta ad incidenti in cui due sistemi comunicano.
* **Descrizione**: 
    - Creazione di un server di gestione utilizzando `FastAPI`.
	- Implementazione di playbook per gestire il login.
	- Modifica dello stato degli utenti.

### Laboratorio 4: Scrittura di una libreria per la gestione firewall
* **Obiettivo**: Sviluppare una libreria Python per la gestione programmata delle regole firewall.
* **Descrizione**: 
    - Creazione, modifica e cancellazione di regole firewall.
    - Automazione della configurazione firewall per migliorare la sicurezza di rete.

### Laboratorio 5: Lettura del file eve.json di Suricata per la creazione di regole
* **Obiettivo**: Automatizzare la generazione di regole firewall basate sugli eventi rilevati da Suricata.
* **Descrizione**: 
    - Parsing del file `eve.json` prodotto da Suricata.
    - Estrazione di informazioni rilevanti per la creazione dinamica di regole firewall.

---

## Requisiti Tecnici
Per eseguire gli script presenti in questa repository, installare le dipendenze tramite il file `requirements.txt`:

```bash
pip install -r requirements.txt
```

---
*Repository mantenuta per scopi didattici.*
