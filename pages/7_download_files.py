import streamlit as st
import sqlite3
import os
from datetime import datetime

st.set_page_config(page_title="📤 Muat Naik Fail Kursus", layout="centered")
st.title("📤 Muat Naik Fail Kursus")

# Semak login
if "user_id" not in st.session_state or "role" not in st.session_state:
    st.error("Sila log masuk terlebih dahulu.")
    st.stop()

# Sambungan ke pangkalan data
def create_connection():
    return sqlite3.connect("database/stattrack_official.db", check_same_thread=False)

conn = create_connection()
c = conn.cursor()

# ✅ Semua pensyarah/admin boleh akses semua kursus
c.execute("SELECT course_code, course_name FROM courses")
courses = c.fetchall()
course_dict = {code: name for code, name in courses}

if not course_dict:
    st.warning("Tiada kursus tersedia.")
    st.stop()

# 📂 Dapatkan kategori fail
c.execute("SELECT category_id, category_name FROM file_categories")
categories = c.fetchall()
category_dict = {cid: cname for cid, cname in categories}

# 📝 Borang muat naik
selected_course = st.selectbox("📘 Pilih Kursus", list(course_dict.keys()), format_func=lambda x: f"{x} - {course_dict[x]}")
selected_category = st.selectbox("🗂️ Pilih Kategori Fail", list(category_dict.keys()), format_func=lambda x: category_dict[x])

# 🔎 Semak subkategori
c.execute("SELECT subcategory_name FROM file_subcategories WHERE category_id = ?", (selected_category,))
subcategories = [row[0] for row in c.fetchall()]
selected_subcategory = None
if subcategories:
    selected_subcategory = st.selectbox("📌 Pilih Subkategori", subcategories)

uploaded_file = st.file_uploader("📎 Muat Naik Fail", type=["pdf", "docx", "xlsx", "png", "jpg"])

if uploaded_file:
    # Simpan fail
    UPLOAD_DIR = "uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{selected_course}_{selected_category}_{timestamp}_{uploaded_file.name}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())

    # Simpan ke DB
    c.execute("""
        INSERT INTO uploaded_files (course_code, category_id, filename, uploaded_by, upload_date, file_path, subcategory_name)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        selected_course,
        selected_category,
        uploaded_file.name,
        st.session_state["user_id"],
        timestamp,
        filepath,
        selected_subcategory
    ))
    conn.commit()

    st.success(f"✅ Fail **{uploaded_file.name}** berjaya dimuat naik.")
