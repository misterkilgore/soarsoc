import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configurazione della pagina
st.set_page_config(page_title="Ticket Dashboard", layout="wide")

# Titolo
st.title("📊 Gestione Ticket")

# Caricamento dati
df = pd.read_csv("tickets.csv", index_col=0)

# 1. Visualizzazione tabella con colori per severity
st.header("📋 Lista Ticket")

def color_rows(row):
    if row['severity'] == 'HIGH':
        return ['background-color: #ff9999'] * len(row)  # rosso chiaro
    elif row['severity'] == 'MEDIUM':
        return ['background-color: #fff099'] * len(row)  # giallo chiaro
    elif row['severity'] == 'LOW':
        return ['background-color: #b3ffb3'] * len(row)  # verde chiaro
    else:
        return [''] * len(row)

st.dataframe(
    df.style.apply(color_rows,axis=1),
    use_container_width=True,
    height=400
    )

# 2. Modifica dello status
st.header("✏️ Modifica Status Ticket")

# Selezione ticket
ticket_ids = df.index.tolist()
selected_ticket = st.selectbox("Seleziona ID Ticket", ticket_ids)

if selected_ticket is not None:
    current_status = df.loc[selected_ticket, 'status']
    new_status = st.selectbox(
        "Nuovo Status",
        ["OPEN", "WIP", "CLOSED"],
        index=["OPEN", "WIP", "CLOSED"].index(current_status)
    )
    
    if st.button("Aggiorna Status"):
        df.loc[selected_ticket, 'status'] = new_status
        df.to_csv("tickets.csv")
        st.success(f"Ticket {selected_ticket} aggiornato a {new_status}")
        st.rerun()

# 3. Grafici
st.header("📈 Analisi Ticket")

col1, col2 = st.columns(2)

with col1:
    status_counts = df['status'].value_counts()
    colors = {'OPEN': 'blue', 'WIP': 'orange', 'CLOSED': 'green'}
    fig, ax = plt.subplots()
    bars = ax.bar(status_counts.index, status_counts.values, color=[colors.get(x, 'gray') for x in status_counts.index])
    ax.set_title("Ticket per Status")
    ax.set_xlabel("Status")
    ax.set_ylabel("Count")
    st.pyplot(fig)

with col2:
    severity_counts = df['severity'].value_counts()
    colors = {'LOW': 'lightgreen', 'MEDIUM': 'orange', 'HIGH': 'red'}
    fig, ax = plt.subplots()
    bars = ax.bar(severity_counts.index, severity_counts.values, color=[colors.get(x, 'gray') for x in severity_counts.index])
    ax.set_title("Ticket per Severity")
    ax.set_xlabel("Severity")
    ax.set_ylabel("Count")
    st.pyplot(fig)