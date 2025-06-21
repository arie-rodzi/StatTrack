import streamlit as st
import sqlite3
import os
from datetime import datetime

# Konfigurasi asas
st.set_page_config(page_title="Muat Naik Fail Kursus", layout="centered")
st.title("📤 Muat Naik Fail Kursus")

# Pastikan pengguna log masuk dan betul role
if "user_id" not in st.session_state or st.session_state["role"] not in ["admin", "lecturer"]:
    st.warning("Modul ini hanya untuk pensyarah dan pentadbir.")
    st.stop()

# Sambungan ke pangkalan data
def create_connection():
    return sqlite3.connect("database/stattrack_official.db", check_same_thread=False)

conn = create_connection()
c = conn.cursor()

# Dapatkan kursus yang berkaitan dengan pensyarah ini
if st.session_state["role"] == "lecturer":
    c.execute("SELECT course_code, course_name FROM courses WHERE assigned_lecturer = ?", (st.session_state["user_id"],))
else:
    c.execute("SELECT course_code, course_name FROM courses")  # admin boleh pilih semua

courses = c.fetchall()
course_dict = {code: name for code, name in courses}

if not course_dict:
    st.warning("Tiada kursus dijumpai. Sila hubungi admin.")
    st.stop()

# Dapatkan kategori fail
c.execute("SELECT category_id, category_name FROM file_categories")
categories = c.fetchall()
category_dict = {cid: cname for cid, cname in categories}

# Borang muat naik
selected_course = st.selectbox("Pilih Kursus", list(course_dict.keys()), format_func=lambda x: f"{x} - {course_dict[x]}")
selected_category = st.selectbox("Jenis Fail", list(category_dict.keys()), format_func=lambda x: category_dict[x])
uploaded_file = st.file_uploader("Muat Naik Fail", type=["pdf", "docx", "xlsx"])

if uploaded_file:
    UPLOAD_DIR = "uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Simpan fail ke dalam folder
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{selected_course}_{selected_category}_{timestamp}_{uploaded_file.name}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())

    # Simpan rekod dalam DB
    c.execute("""
        INSERT INTO uploaded_files (course_code, category_id, filename, uploaded_by, upload_date, file_path)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (selected_course, selected_category, uploaded_file.name, st.session_state["user_id"], timestamp, filepath))
    conn.commit()

    st.success(f"Fail **{uploaded_file.name}** berjaya dimuat naik.")
# Placeholder for 4_upload_file.py
