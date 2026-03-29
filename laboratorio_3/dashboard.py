import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Security Admin Panel", layout="centered")

st.title("🛡️ Monitoraggio Accessi Utenti")

def load_data():
    conn = sqlite3.connect('sicurezza.db')
    df = pd.read_sql_query("SELECT * FROM utenti", conn)
    conn.close()
    return df

df = load_data()

# Visualizzazione con colori condizionali
def highlight_status(val):
    color = 'red' if val == 'BLOCKED' else 'green'
    return f'color: {color}; font-weight: bold'

st.table(df.style.applymap(highlight_status, subset=['stato']))

if st.button('Aggiorna Dati'):
    st.rerun()