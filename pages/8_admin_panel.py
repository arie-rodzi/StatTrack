# Placeholder for 8_admin_panel.py
import streamlit as st
import sqlite3

st.set_page_config(page_title="Panel Admin", layout="centered")
st.title("⚙️ Panel Admin StatTrack")

# Pastikan hanya admin boleh akses
if "user_id" not in st.session_state or st.session_state["role"] != "admin":
    st.warning("Modul ini hanya untuk pentadbir.")
    st.stop()

# Sambung ke database
def create_connection():
    return sqlite3.connect("database/stattrack_official.db", check_same_thread=False)

conn = create_connection()
c = conn.cursor()

st.header("➕ Tambah Pengguna Baru")

with st.form("add_user_form"):
    new_user_id = st.text_input("ID Pengguna (user_id)")
    new_name = st.text_input("Nama Penuh")
    new_password = st.text_input("Katalaluan Awal", type="password")
    new_role = st.selectbox("Peranan", ["admin", "lecturer", "student"])
    submitted = st.form_submit_button("Tambah Pengguna")

    if submitted:
        import hashlib
        hashed = hashlib.sha256(new_password.encode()).hexdigest()
        try:
            c.execute("INSERT INTO users (user_id, name, password_hash, role, force_register) VALUES (?, ?, ?, ?, 1)", 
                      (new_user_id, new_name, hashed, new_role))
            conn.commit()
            st.success("Pengguna berjaya ditambah.")
        except sqlite3.IntegrityError:
            st.error("ID Pengguna sudah wujud.")

st.markdown("---")
st.header("📘 Tambah Kursus")

with st.form("add_course_form"):
    course_code = st.text_input("Kod Kursus")
    course_name = st.text_input("Nama Kursus")
    program_code = st.text_input("Kod Program")
    
    # Dapatkan senarai pensyarah sahaja
    c.execute("SELECT user_id, name FROM users WHERE role = 'lecturer'")
    lecturers = c.fetchall()
    lecturer_dict = {uid: name for uid, name in lecturers}
    selected_lecturer = st.selectbox("Pilih Pensyarah", list(lecturer_dict.keys()), format_func=lambda x: f"{x} - {lecturer_dict[x]}")
    
    submitted_course = st.form_submit_button("Tambah Kursus")

    if submitted_course:
        try:
            c.execute("INSERT INTO courses (course_code, course_name, program_code, assigned_lecturer) VALUES (?, ?, ?, ?)", 
                      (course_code, course_name, program_code, selected_lecturer))
            conn.commit()
            st.success("Kursus berjaya ditambah.")
        except sqlite3.IntegrityError:
            st.error("Kod kursus sudah wujud.")

st.markdown("---")
st.header("🗂️ Tambah Kategori Fail")

with st.form("add_category_form"):
    category_name = st.text_input("Nama Kategori Fail")
    submitted_cat = st.form_submit_button("Tambah Kategori")

    if submitted_cat:
        c.execute("INSERT INTO file_categories (category_name) VALUES (?)", (category_name,))
        conn.commit()
        st.success("Kategori berjaya ditambah.")
