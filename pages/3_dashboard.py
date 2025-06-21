import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Senarai Kursus (Awal)", layout="wide")
st.title("📘 Paparan Senarai Kursus: LIC & RP")

def create_connection():
    return sqlite3.connect("database/stattrack_official.db", check_same_thread=False)

conn = create_connection()

# Ambil semua kursus (LIC)
df_courses = pd.read_sql_query("SELECT course_code, course_name, program_code, assigned_lecturer FROM courses", conn)

# Ambil semua uploaded_by (RP)
df_rp = pd.read_sql_query("SELECT DISTINCT course_code, uploaded_by FROM uploaded_files", conn)

# Gabung ikut course_code
df_merge = pd.merge(df_courses, df_rp, on="course_code", how="left")  # kekalkan semua kursus walau tiada RP

# Tukar nama kolum
df_merge = df_merge.rename(columns={
    "course_code": "Kod Kursus",
    "course_name": "Nama Kursus",
    "program_code": "Program",
    "assigned_lecturer": "Pensyarah LIC",
    "uploaded_by": "Pensyarah RP"
})

# Tapis ikut program (jika wujud)
if "Program" in df_merge.columns and not df_merge["Program"].dropna().empty:
    pilihan_program = sorted(df_merge["Program"].dropna().unique().tolist())
    selected_program = st.selectbox("🎓 Tapis Mengikut Program", ["Semua"] + pilihan_program)
    if selected_program != "Semua":
        df_merge = df_merge[df_merge["Program"] == selected_program]

# Susun kolum
ordered_cols = ["Kod Kursus", "Nama Kursus", "Program", "Pensyarah LIC", "Pensyarah RP"]
df_merge = df_merge[ordered_cols]

# Papar
if not df_merge.empty:
    st.dataframe(df_merge, use_container_width=True)
else:
    st.info("Tiada data untuk dipaparkan.")

conn.close()
