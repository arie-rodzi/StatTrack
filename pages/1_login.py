import streamlit as st
import sqlite3
import hashlib

# Fungsi untuk has kata laluan
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fungsi sambungan ke database
def create_connection():
    return sqlite3.connect("database/stattrack_official.db", check_same_thread=False)

# Fungsi login guna user_id
def login_user(user_id, password):
    conn = create_connection()
    c = conn.cursor()
    hashed = hash_password(password)
    c.execute("SELECT user_id, name, password_hash, role, force_register FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row and row[2] == hashed:
        return {
            "user_id": row[0],
            "name": row[1],
            "role": row[3],
            "force_register": row[4]
        }
    return None

# Konfigurasi paparan halaman
st.set_page_config(page_title="StatTrack Login", layout="centered")
st.title("📊 Log Masuk Sistem StatTrack")

# Input login
user_id = st.text_input("ID Pengguna (user_id)")
password = st.text_input("Katalaluan", type="password")

# Butang log masuk
if st.button("Log Masuk"):
    user = login_user(user_id, password)
    if user:
        # Simpan dalam session
        st.session_state['user_id'] = user["user_id"]
        st.session_state['name'] = user["name"]
        st.session_state['role'] = user["role"]

        if user["force_register"] == 1:
            st.success("Sila tukar katalaluan terlebih dahulu.")
            st.switch_page("pages/2_register_first_time.py")
        else:
            st.success(f"Selamat datang, {user['name']}!")
            st.switch_page("pages/3_dashboard.py")
    else:
        st.error("ID Pengguna atau Katalaluan salah.")
