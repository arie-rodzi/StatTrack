import streamlit as st
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_connection():
    return sqlite3.connect("database/stattrack_official.db", check_same_thread=False)

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

# UI
st.set_page_config(page_title="Log Masuk StatTrack", layout="centered")
st.title("📊 Log Masuk Sistem StatTrack")

user_id = st.text_input("ID Pengguna")
password = st.text_input("Katalaluan", type="password")

if st.button("Log Masuk"):
    user = login_user(user_id, password)
    if user:
        st.session_state['user_id'] = user["user_id"]
        st.session_state['name'] = user["name"]
        st.session_state['role'] = user["role"]

        if user["force_register"] == 1:
            st.success("Sila tukar katalaluan terlebih dahulu.")
            st.switch_page("pages/2_register_first_time.py")
        else:
            st.success(f"Selamat datang, {user['name']}!")
            st.switch_page("pages/3_course_overview.py")
    else:
        st.error("ID Pengguna atau Katalaluan salah.")
