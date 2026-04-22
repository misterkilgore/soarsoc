import streamlit as st
import requests

st.title("Invio Ticket a n8n")

with st.form("ticket_form"):
    nome_operatore = st.text_input("Nome operatore")
    priorita = st.selectbox("Priorità", options=["Bassa", "Media", "Alta", "Critica"])
    ip = st.text_input("IP")
    descrizione = st.text_area("Descrizione problema")
    n8n_url = st.text_input("URL webhook n8n (es. https://tuo-n8n-webhook-url)")

    submitted = st.form_submit_button("Invia Ticket")

if submitted:
    if not nome_operatore or not ip or not descrizione or not n8n_url:
        st.error("Per favore, compila tutti i campi obbligatori, incluso l'URL.")
    else:
        payload = {
            "nome_operatore": nome_operatore,
            "priorita": priorita,
            "ip": ip,
            "descrizione": descrizione
        }

        try:
            response = requests.post(n8n_url, json=payload)
            if response.status_code == 200:
                st.success("Ticket inviato con successo!")
            else:
                st.error(f"Errore nell'invio: {response.status_code} {response.text}")
        except Exception as e:
            st.error(f"Errore di connessione: {e}")