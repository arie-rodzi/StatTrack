import streamlit as st
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_connection():
    return sqlite3.connect("database/stattrack_official.db", check_same_thread=False)

def update_password(user_id, new_password):
    conn = create_connection()
    c = conn.cursor()
    new_hash = hash_password(new_password)
    c.execute("UPDATE users SET password_hash = ?, force_register = 0 WHERE user_id = ?", (new_hash, user_id))
    conn.commit()
    conn.close()

st.set_page_config(page_title="Tukar Katalaluan", layout="centered")
st.title("🔐 Tukar Katalaluan Kali Pertama")

if "user_id" not in st.session_state:
    st.warning("Sila log masuk terlebih dahulu.")
    st.stop()

new_pass = st.text_input("Katalaluan Baru", type="password")
confirm_pass = st.text_input("Sahkan Katalaluan", type="password")

if st.button("Kemaskini"):
    if new_pass != confirm_pass:
        st.error("Katalaluan tidak sepadan.")
    elif len(new_pass) < 6:
        st.error("Katalaluan mesti sekurang-kurangnya 6 aksara.")
    else:
        update_password(st.session_state["user_id"], new_pass)
        st.success("Katalaluan berjaya ditukar.")
        st.switch_page("pages/3_dashboard.py")
# Placeholder for 2_register_first_time.py
