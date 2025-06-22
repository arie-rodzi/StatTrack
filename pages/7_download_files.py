import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="📥 Semakan & Muat Turun Fail", layout="wide")
st.title("📥 Semakan & Muat Turun Fail Kursus")

# Semak login
if "user_id" not in st.session_state or "role" not in st.session_state:
    st.error("Sila log masuk terlebih dahulu.")
    st.stop()

# Sambungan DB
def create_connection():
    return sqlite3.connect("database/stattrack_official.db", check_same_thread=False)

conn = create_connection()
c = conn.cursor()

# Papar senarai semua kategori & subkategori
c.execute("SELECT category_id, category_name FROM file_categories")
category_dict = {cid: cname for cid, cname in c.fetchall()}

# Pilihan jenis capaian
filter_type = st.radio("🔍 Pilih Kaedah Carian Fail", ["Semua Subjek", "Mengikut Program", "Subjek Individu"], horizontal=True)

# Muatkan semua data kursus
c.execute("SELECT course_code, course_name, program_code FROM courses")
all_courses = c.fetchall()
course_dict = {code: (name, prog) for code, name, prog in all_courses}

filtered_courses = []

if filter_type == "Semua Subjek":
    filtered_courses = list(course_dict.keys())
elif filter_type == "Mengikut Program":
    selected_program = st.selectbox("🏫 Pilih Program", sorted(set(p for _, (_, p) in course_dict.items())))
    filtered_courses = [code for code, (_, prog) in course_dict.items() if prog == selected_program]
elif filter_type == "Subjek Individu":
    selected_course = st.selectbox("📘 Pilih Subjek", list(course_dict.keys()), format_func=lambda x: f"{x} - {course_dict[x][0]}")
    filtered_courses = [selected_course]

# Pilihan jenis fail
filter_category = st.selectbox("🗂️ Tapis Kategori Fail (Optional)", ["Semua"] + list(category_dict.values()))

# Papar semua fail yang ditapis
query = "SELECT course_code, category_id, subcategory_name, filename, uploaded_by, upload_date, file_path FROM uploaded_files"
c.execute(query)
rows = c.fetchall()

df = pd.DataFrame(rows, columns=["Kod Kursus", "ID Kategori", "Subkategori", "Nama Fail", "Pemuat Naik", "Tarikh", "Path"])
df["Nama Kursus"] = df["Kod Kursus"].apply(lambda x: course_dict[x][0] if x in course_dict else x)
df["Program"] = df["Kod Kursus"].apply(lambda x: course_dict[x][1] if x in course_dict else "N/A")
df["Kategori"] = df["ID Kategori"].apply(lambda x: category_dict.get(x, "Tidak Diketahui"))

# Tapis ikut subjek
df = df[df["Kod Kursus"].isin(filtered_courses)]

# Tapis ikut kategori jika dipilih
if filter_category != "Semua":
    df = df[df["Kategori"] == filter_category]

# Papar jadual
if df.empty:
    st.warning("Tiada fail dijumpai untuk pilihan yang ditapis.")
else:
    st.dataframe(df[["Kod Kursus", "Nama Kursus", "Kategori", "Subkategori", "Nama Fail", "Pemuat Naik", "Tarikh"]])

    # Pilihan muat turun
    for i, row in df.iterrows():
        with open(row["Path"], "rb") as f:
            st.download_button(
                label=f"📥 Muat Turun {row['Nama Fail']} ({row['Kod Kursus']})",
                data=f,
                file_name=row["Nama Fail"],
                mime="application/octet-stream",
                key=f"download_{i}"
            )
