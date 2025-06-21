import streamlit as st
from database import init_db

st.set_page_config(page_title="StatTrack – Fail Kursus Statistik", layout="wide")
st.title("📊 StatTrack – Sistem Fail Kursus Statistik")

st.markdown("""
Selamat datang ke **StatTrack**, sistem pengurusan dan pemantauan fail kursus bagi pensyarah Statistik dan Matematik di UiTM.
Sila gunakan menu di sebelah kiri untuk login, daftar kali pertama, atau akses sebagai admin.
""")

init_db()