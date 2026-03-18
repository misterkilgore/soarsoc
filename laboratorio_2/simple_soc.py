import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione della pagina
st.set_page_config(page_title="Ticket Dashboard", layout="wide")

# Titolo
st.title("📊 Gestione Ticket")

# Caricamento dati
df = pd.read_csv("tickets.csv", index_col=0)

# 1. Visualizzazione tabella con colori per severity
st.header("📋 Lista Ticket")

# Funzione per colorare le righe in base alla severity
def color_severity(row):
    colors = {
        'LOW': 'background-color: lightgreen',
        'MEDIUM': 'background-color: orange',
        'HIGH': 'background-color: lightcoral'
    }
    return [colors.get(row['severity'], '')] * len(row)

# Mostra tabella con colori
st.dataframe(
    df.style.apply(color_severity, axis=1),
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
    # Grafico per status
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    fig_status = px.bar(status_counts, x='status', y='count', 
                        title="Ticket per Status",
                        color='status',
                        color_discrete_map={'OPEN': 'blue', 'WIP': 'orange', 'CLOSED': 'green'})
    st.plotly_chart(fig_status, use_container_width=True)

with col2:
    # Grafico per severity
    severity_counts = df['severity'].value_counts().reset_index()
    severity_counts.columns = ['severity', 'count']
    fig_severity = px.bar(severity_counts, x='severity', y='count',
                          title="Ticket per Severity",
                          color='severity',
                          color_discrete_map={'LOW': 'lightgreen', 'MEDIUM': 'orange', 'HIGH': 'red'})
    st.plotly_chart(fig_severity, use_container_width=True)