import streamlit as st
import google.generativeai as genai
import json
import base64
import os

# Memanggil modul-modul eksternal
from modules import puasa
from modules import nutrisi   
from modules import olga

# --- 1. Konfigurasi Halaman ---
st.set_page_config(page_title="Konsultan Hidup Sehat", page_icon="🌱", layout="centered", initial_sidebar_state="collapsed")

# --- SCRIPT PENGHILANG MENU, SIDEBAR, & CSS ---
hide_menu_style = """
<style>
#MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
[data-testid="collapsedControl"] {display: none !important;}
[data-testid="stSidebar"] {display: none !important;} section[data-testid="stSidebar"] {display: none !important;}
[data-testid="stToolbar"] {display: none !important;} [data-testid="stDecoration"] {display: none !important;}
[data-testid="stStatusWidget"] {display: none !important;} div[class*="viewerBadge"] {display: none !important;}
.block-container { padding-top: 2rem !important; padding-bottom: 150px !important; }
h3 { color: #0066cc; border-bottom: 2px solid #f0f2f6; padding-bottom: 5px; margin-top: 25px; }
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# --- FUNGSI PARSING JSON AI ---
def parse_ai_json(teks_respon):
    try:
        clean_json = teks_respon.strip().replace('```json', '').replace('```', '')
        return json.loads(clean_json)
    except Exception as e:
        return None

# --- 2. FUNGSI GATEKEEPER (GERBANG TOL) ---
def cek_password():
    logo_path = "Logo_Aplikasi_Sehat.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            
        html_logo = f"""
        <div style="display: flex; justify-content: center; margin-bottom: 15px;">
            <div style="background-color: white; border: 4px solid #DAA520; border-radius: 50%; width: 130px; height: 130px; display: flex; justify-content: center; align-items: center; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5); overflow: hidden;">
                <img src="data:image/png;base64,{encoded_string}" style="width: 75%; height: auto;">
            </div>
        </div>
        """
        st.markdown(html_logo, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; margin-top: -10px;'>🌱 Konsultan Hidup Sehat</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: #FFFFFF; font-weight: normal; font-size: 15px; margin-bottom: 20px; line-height: 1.4;'>Panduan Puasa Intermiten sesuai Usia, Jenis Kelamin, Komposisi Tubuh, dan Riwayat Kesehatan</h5>", unsafe_allow_html=True)
    st.divider()

    if "PASSWORD_AKSES" not in st.secrets:
        st.error("⚠️ Konfigurasi Server Belum Lengkap.")
        st.stop()

    input_pass = st.text_input("🔑 Masukkan Kode Akses Premium:", type="password", placeholder="Ketik kode akses Anda di sini...")
    tombol_akses = st.button("Buka Akses Aplikasi", type="primary", use_container_width=True)

    if input_pass != st.secrets["PASSWORD_AKSES"]:
        if input_pass or tombol_akses:
            if input_pass: st.error("⛔ Kode Akses Salah!")
            else: st.error("⚠️ Silakan ketik kode akses terlebih dahulu!")
        
        st.info("🔒 Aplikasi ini dikunci khusus untuk Member Premium.")
        st.link_button("🛒 Beli Kode Akses (Klik Disini)", "https://lynk.id/hahastoresby", type="primary", use_container_width=True)
        st.write("\n" * 5) 
        st.stop()
    
    st.success("✅ Akses Diterima!")

cek_password()

# --- CEK API KEY ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-flash-latest')
else:
    st.error("⚠️ API Key belum dipasang. Cek Secrets.")
    st.stop()

# =========================================================================
# NAVIGASI MENU UTAMA
# =========================================================================
st.markdown("### 🧭 Menu Utama")
menu_app = st.selectbox(
    "Silakan pilih modul yang ingin dibuka:",
    [
        "1️⃣ Profil Data Diri", 
        "2️⃣ Panduan Puasa (IF) & Autofagi", 
        "3️⃣ Modul Nutrisi & Superfood", 
        "4️⃣ Modul Olahraga"
    ]
)
st.divider()

# =========================================================================
# MODUL 1: PROFIL DATA DIRI (HANYA FORM)
# =========================================================================
if menu_app == "1️⃣ Profil Data Diri":
    st.markdown("### 📝 Lengkapi Data Diri Anda")

    st.subheader("1️⃣ Data Fisik")
    nama = st.text_input("Nama Panggilan", st.session_state.get('user_profile', {}).get('nama', "Sobat Sehat"))

    col1, col2 = st.columns(2)
    with col1:
        usia = st.number_input("Usia (Tahun)", 15, 100, st.session_state.get('user_profile', {}).get('usia', 41))
        berat = st.number_input("Berat (kg)", 30.0, 150.0, st.session_state.get('user_profile', {}).get('berat', 70.0))
    with col2:
        gender_index = 0 if st.session_state.get('user_profile', {}).get('gender', "Laki-laki") == "Laki-laki" else 1
        gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"], index=gender_index)
        tinggi = st.number_input("Tinggi (cm)", 100.0, 250.0, st.session_state.get('user_profile', {}).get('tinggi', 170.0))

    st.subheader("2️⃣ Pengalaman Puasa")
    pengalaman_puasa = st.radio("Apakah Anda sudah biasa berpuasa intermiten?", ["Iya", "Baru akan mencoba", "Sudah pernah tapi sudah berhenti"])
    lama_berhenti = st.text_input("Sudah berhenti berapa lama? (dalam bulan)") if pengalaman_puasa == "Sudah pernah tapi sudah berhenti" else ""
    butuh_panduan_pemula = st.radio("Apakah Anda memerlukan Panduan Aman untuk Mulai Berpuasa bagi Pemula?", ["Iya", "Tidak"])

    st.subheader("3️⃣ Riwayat Kesehatan")
    kondisi = st.text_area("Kondisi Kesehatan:", st.session_state.get('user_profile', {}).get('kondisi', "Ceritakan kondisi kesehatan Anda yang terakhir."), height=70)

    st.subheader("4️⃣ Pertanyaan Anda")
    pertanyaan = st.text_area("Keluhan/Pertanyaan:", st.session_state.get('user_profile', {}).get('pertanyaan', "Bagaimana cara mulai puasa yang aman?"), height=100)

    # TOMBOL SIMPAN KE KOPER DIGITAL
    if st.button("💾 Simpan Data Profil", type="primary", use_container_width=True):
        bmi = berat / ((tinggi/100)**2)
        st.session_state['user_profile'] = {
            "nama": nama, "usia": usia, "gender": gender, "tinggi": tinggi, "berat": berat,
            "bmi": bmi, "pengalaman_puasa": pengalaman_puasa, "lama_berhenti": lama_berhenti, 
            "butuh_panduan_pemula": butuh_panduan_pemula, "kondisi": kondisi, "pertanyaan": pertanyaan
        }
        st.success("✅ Data Profil berhasil disimpan! Silakan pilih menu **2️⃣ Panduan Puasa (IF)** di atas.")

# =========================================================================
# ROUTING KE MODUL-MODUL LAINNYA
# =========================================================================
elif menu_app == "2️⃣ Panduan Puasa (IF) & Autofagi":
    puasa.render_halaman(model)

elif menu_app == "3️⃣ Modul Nutrisi & Superfood":
    nutrisi.render_halaman(model, parse_ai_json)

elif menu_app == "4️⃣ Modul Olahraga":
    olga.render_halaman(model, parse_ai_json)
