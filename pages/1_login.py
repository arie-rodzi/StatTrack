import streamlit as st
from database import get_connection
from utils import hash_password, verify_password

def login_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT password_hash, role FROM users WHERE user_id = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result and verify_password(password, result[0]):
        return result[1]
    return None

st.title("🔐 Log Masuk Pensyarah / Admin")
username = st.text_input("ID Pengguna (No Staf)")
password = st.text_input("Katalaluan", type="password")
if st.button("Log Masuk"):
    role = login_user(username, password)
    if role:
        st.session_state.logged_in = True
        st.session_state.user_id = username
        st.session_state.role = role
        st.success(f"Selamat datang, {username}!")
        st.experimental_rerun()
    else:
        st.error("ID atau katalaluan salah.")
