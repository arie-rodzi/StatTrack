import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Senarai Kursus", layout="wide")
st.title("📘 Paparan Senarai Kursus (LIC / RP)")

# Sambungan ke pangkalan data
def create_connection():
    return sqlite3.connect("database/stattrack_official.db", check_same_thread=False)

conn = create_connection()

# Baca data dari jadual course_roles
df = pd.read_sql_query("SELECT * FROM course_roles", conn)

conn.close()

# Tapis mengikut program jika ada
if 'program' in df.columns and not df['program'].dropna().empty:
    all_programs = sorted(df['program'].dropna().unique().tolist())
    selected_program = st.selectbox("🎓 Tapis Mengikut Program", ["Semua"] + all_programs)
    if selected_program != "Semua":
        df = df[df['program'] == selected_program]

# Tukar nama kolum untuk paparan
df = df.rename(columns={
    "course_code": "Kod Kursus",
    "course_name": "Nama Kursus",
    "program": "Program",
    "role": "Peranan",
    "lecturer_name": "Nama Pensyarah",
    "duration": "Tempoh Lantikan"
})

# Susun kolum
ordered_columns = ["Kod Kursus", "Nama Kursus", "Program", "Peranan", "Nama Pensyarah", "Tempoh Lantikan"]
df = df[ordered_columns]

# Paparkan DataFrame
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("Tiada data untuk dipaparkan.")
