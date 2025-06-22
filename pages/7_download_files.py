import streamlit as st
import sqlite3
import os
import zipfile

st.set_page_config(page_title="📥 Muat Turun Fail Kursus", layout="wide")
st.title("📥 Muat Turun Fail Kursus")

# Semak login
if "user_id" not in st.session_state or "role" not in st.session_state:
    st.error("Sila log masuk terlebih dahulu.")
    st.stop()

# Sambung DB
def create_connection():
    return sqlite3.connect("database/stattrack_official.db", check_same_thread=False)

conn = create_connection()
c = conn.cursor()

# Kursus yang pensyarah dilantik sebagai RP/LIC
c.execute("""
    SELECT DISTINCT course_code, course_name
    FROM course_roles
    WHERE UPPER(lecturer_name) = UPPER(?)
    AND role IN ('RP', 'LIC')
""", (st.session_state["name"],))
courses = c.fetchall()
course_dict = {code: name for code, name in courses}

if not course_dict:
    st.warning("Anda tidak dilantik sebagai RP atau LIC.")
    st.stop()

selected_course = st.selectbox("📘 Pilih Kursus", list(course_dict.keys()), format_func=lambda x: f"{x} - {course_dict[x]}")

# Pilih kategori
c.execute("SELECT category_id, category_name FROM file_categories")
categories = c.fetchall()
category_dict = {cid: cname for cid, cname in categories}
selected_category = st.selectbox("🗂️ Pilih Kategori", list(category_dict.keys()), format_func=lambda x: category_dict[x])

# Pilih subkategori (jika ada)
c.execute("SELECT subcategory_name FROM file_subcategories WHERE category_id = ?", (selected_category,))
subcats = [row[0] for row in c.fetchall()]
selected_subcategory = None
if subcats:
    selected_subcategory = st.selectbox("📌 Pilih Subkategori", subcats)

# Ambil senarai fail
if selected_subcategory:
    c.execute("""
        SELECT filename, file_path FROM uploaded_files
        WHERE course_code = ? AND category_id = ? AND uploaded_by = ? AND subcategory_name = ?
    """, (selected_course, selected_category, st.session_state["user_id"], selected_subcategory))
else:
    c.execute("""
        SELECT filename, file_path FROM uploaded_files
        WHERE course_code = ? AND category_id = ? AND uploaded_by = ?
    """, (selected_course, selected_category, st.session_state["user_id"]))

files = c.fetchall()

if not files:
    st.info("Tiada fail ditemui.")
else:
    st.markdown("### 📄 Senarai Fail Ditemui")
    for fname, fpath in files:
        with open(fpath, "rb") as f:
            st.download_button(f"📥 Muat Turun: {fname}", f.read(), file_name=fname)

    # Sediakan muat turun ZIP jika lebih dari 1
    if len(files) > 1:
        zip_path = f"downloads/{selected_course}_{selected_category}_all.zip"
        os.makedirs("downloads", exist_ok=True)
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for fname, fpath in files:
                zipf.write(fpath, arcname=os.path.basename(fpath))
        with open(zip_path, "rb") as zf:
            st.download_button("📦 Muat Turun Semua (ZIP)", zf.read(), file_name=os.path.basename(zip_path), mime="application/zip")

conn.close()
# Placeholder for 7_download_files.py
