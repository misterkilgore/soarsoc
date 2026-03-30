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

---

## Requisiti Tecnici
Per eseguire gli script presenti in questa repository, è necessario avere installato:
* Python 3.x
* Libreria Pandas (`pip install pandas`)
* SQLite (integrato in Python)

---
*Repository mantenuta per scopi didattici.*
