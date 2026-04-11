import streamlit as st
import sqlite3
import subprocess

# Database setup
def init_db():
    conn = sqlite3.connect('iptables_rules.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rules (
                    id INTEGER PRIMARY KEY,
                    chain TEXT,
                    rule TEXT
                )''')
    conn.commit()
    conn.close()

# Add rule to DB and apply to iptables
def add_rule(chain, rule):
    conn = sqlite3.connect('iptables_rules.db')
    c = conn.cursor()
    c.execute("INSERT INTO rules (chain, rule) VALUES (?, ?)", (chain, rule))
    conn.commit()
    conn.close()
    # Apply to iptables
    try:
        subprocess.run(['iptables', '-A', chain] + rule.split(), check=True)
        st.success("Rule applied to iptables")
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to apply rule to iptables: {e}")
    except FileNotFoundError:
        st.warning("iptables command not found. Rule saved to database only.")

# List rules from DB
def list_rules():
    conn = sqlite3.connect('iptables_rules.db')
    c = conn.cursor()
    c.execute("SELECT id, chain, rule FROM rules")
    rules = c.fetchall()
    conn.close()
    return rules

# Delete rule from DB and iptables
def delete_rule(rule_id):
    conn = sqlite3.connect('iptables_rules.db')
    c = conn.cursor()
    c.execute("SELECT chain, rule FROM rules WHERE id=?", (rule_id,))
    row = c.fetchone()
    if row:
        chain, rule = row
        # Remove from iptables
        try:
            subprocess.run(['iptables', '-D', chain] + rule.split(), check=True)
            st.success("Rule removed from iptables")
        except subprocess.CalledProcessError as e:
            st.error(f"Failed to remove rule from iptables: {e}")
        except FileNotFoundError:
            st.warning("iptables command not found. Rule removed from database only.")
        c.execute("DELETE FROM rules WHERE id=?", (rule_id,))
        conn.commit()
    conn.close()

# Streamlit UI
st.title("Iptables GUI")

init_db()

# Add rule section
st.header("Add Rule")
chain = st.selectbox("Chain", ["INPUT", "OUTPUT", "FORWARD"])
rule = st.text_input("Rule (e.g., -p tcp --dport 80 -j ACCEPT)")
if st.button("Add Rule"):
    if rule:
        add_rule(chain, rule)
        st.success("Rule added to database")
    else:
        st.error("Please enter a rule")

# List and delete rules
st.header("Existing Rules")
rules = list_rules()
if rules:
    for r in rules:
        col1, col2, col3, col4 = st.columns([1, 2, 4, 2])
        with col1:
            st.write(f"ID: {r[0]}")
        with col2:
            st.write(f"Chain: {r[1]}")
        with col3:
            st.write(f"Rule: {r[2]}")
        with col4:
            if st.button("Delete", key=f"delete_{r[0]}"):
                delete_rule(r[0])
                st.rerun()
else:
    st.write("No rules in database")