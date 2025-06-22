import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="📂 Semakan Fail Kursus", layout="wide")
st.title("📂 Semakan Fail Kursus")

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

st.markdown("## 📁 Fail Dimuat Naik")
c.execute("""
    SELECT fc.category_name, uf.subcategory_name, uf.filename, uf.upload_date
    FROM uploaded_files uf
    JOIN file_categories fc ON uf.category_id = fc.category_id
    WHERE uf.course_code = ? AND uf.uploaded_by = ?
""", (selected_course, st.session_state["user_id"]))
rows = c.fetchall()

if rows:
    df_uploaded = pd.DataFrame(rows, columns=["Kategori", "Subkategori", "Nama Fail", "Tarikh Muat Naik"])
    st.dataframe(df_uploaded, use_container_width=True)
else:
    st.info("Tiada fail dimuat naik untuk kursus ini.")

st.markdown("## ✅ Semakan Kategori & Subkategori")
# Ambil semua kategori & subkategori wajib untuk kursus ini
c.execute("SELECT category_id, category_name FROM file_categories")
categories = c.fetchall()

for cat_id, cat_name in categories:
    c.execute("""
        SELECT subcategory_name FROM file_subcategories
        WHERE category_id = ?
    """, (cat_id,))
    subcats = [row[0] for row in c.fetchall()]
    
    if not subcats:
        # Kalau tiada subkategori, semak terus kategori
        c.execute("""
            SELECT COUNT(*) FROM uploaded_files
            WHERE course_code = ? AND uploaded_by = ? AND category_id = ?
        """, (selected_course, st.session_state["user_id"], cat_id))
        count = c.fetchone()[0]
        status = "✅" if count > 0 else "❌"
        st.write(f"{status} {cat_name}")
    else:
        st.write(f"### {cat_name}")
        for sub in subcats:
            c.execute("""
                SELECT COUNT(*) FROM uploaded_files
                WHERE course_code = ? AND uploaded_by = ? AND category_id = ? AND subcategory_name = ?
            """, (selected_course, st.session_state["user_id"], cat_id, sub))
            count = c.fetchone()[0]
            status = "✅" if count > 0 else "❌"
            st.write(f"- {status} {sub}")

conn.close()
