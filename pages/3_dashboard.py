import streamlit as st

st.set_page_config(page_title="StatTrack Dashboard", layout="centered")
st.title("🏠 Dashboard StatTrack")

# Semak jika pengguna belum login
if "user_id" not in st.session_state:
    st.warning("Sila log masuk terlebih dahulu.")
    st.stop()

# Paparan ringkasan
st.subheader(f"Selamat datang, {st.session_state['name']} 👋")
st.markdown(f"**Peranan:** `{st.session_state['role']}`")

st.markdown("---")

# Menu berdasarkan peranan pengguna
role = st.session_state["role"]

if role == "admin":
    st.markdown("### 📋 Fungsi Pentadbir")
    st.page_link("pages/4_upload_file.py", label="📤 Muat Naik Fail")
    st.page_link("pages/5_view_uploaded_files.py", label="📁 Lihat Semua Fail")
    st.page_link("pages/6_check_completion.py", label="✅ Semakan Fail Siap")
    st.page_link("pages/7_download_files.py", label="⬇️ Muat Turun Fail")
    st.page_link("pages/8_admin_panel.py", label="⚙️ Panel Admin")

elif role == "lecturer":
    st.markdown("### 📚 Fungsi Pensyarah")
    st.page_link("pages/4_upload_file.py", label="📤 Muat Naik Fail Kursus")
    st.page_link("pages/5_view_uploaded_files.py", label="📁 Lihat Fail Anda")
    st.page_link("pages/6_check_completion.py", label="✅ Semakan Fail Lengkap")
    st.page_link("pages/7_download_files.py", label="⬇️ Muat Turun Fail")

elif role == "student":
    st.markdown("### 🎓 Fungsi Pelajar")
    st.page_link("pages/5_view_uploaded_files.py", label="📁 Lihat Fail Kursus")
    st.page_link("pages/7_download_files.py", label="⬇️ Muat Turun Fail")

else:
    st.error("Peranan tidak dikenali. Sila hubungi pentadbir.")
# Placeholder for 3_dashboard.py
