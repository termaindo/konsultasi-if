import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import base64
import os
from datetime import datetime, timedelta, timezone

# --- 1. Konfigurasi Halaman ---
st.set_page_config(
    page_title="Konsultan Hidup Sehat",
    page_icon="🌱",
    layout="centered"
)

# --- SCRIPT PENGHILANG MENU & PEMBERI JARAK AMAN (CSS) ---
hide_menu_style = """
<style>
/* 1. Sembunyikan Header & Menu Utama */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* 2. Sembunyikan Tombol Floating (Target Berbagai Versi) */
[data-testid="stToolbar"] {display: none !important;}
[data-testid="stDecoration"] {display: none !important;}
[data-testid="stStatusWidget"] {display: none !important;}
div[class*="viewerBadge"] {display: none !important;}
.viewerBadge_container__1QSob {display: none !important;}

/* 3. MANUVER JARAK AMAN (PADDING BAWAH) */
/* Memberi ruang kosong 150px di bawah agar tombol Beli tidak tertutup */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 150px !important; 
}

/* 4. PERCANTIK TAMPILAN HEADER DI WEB */
h3 {
    color: #0066cc; /* Warna biru untuk judul di Web */
    border-bottom: 2px solid #f0f2f6;
    padding-bottom: 5px;
    margin-top: 25px;
}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# --- 2. FUNGSI GATEKEEPER (GERBANG TOL) ---
def cek_password():
    """Fungsi untuk memblokir akses jika password salah"""
    
    # --- MENAMPILKAN LOGO DI WEB (LINGKARAN PUTIH & BINGKAI EMAS) ---
    logo_path = "Logo_Aplikasi_Sehat.png"
    if os.path.exists(logo_path):
        # Membaca gambar menjadi Base64 agar bisa diatur presisi dengan HTML/CSS
        with open(logo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            
        html_logo = f"""
        <div style="display: flex; justify-content: center; margin-bottom: 15px;">
            <div style="
                background-color: white; 
                border: 4px solid #DAA520; /* Warna Emas */
                border-radius: 50%; /* Membuatnya bulat sempurna */
                width: 130px; 
                height: 130px; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5); /* Efek bayangan elegan */
                overflow: hidden;">
                <img src="data:image/png;base64,{encoded_string}" style="width: 75%; height: auto;">
            </div>
        </div>
        """
        st.markdown(html_logo, unsafe_allow_html=True)
    
    # Judul Awal & Subjudul 
    st.markdown("<h1 style='text-align: center; margin-top: -10px;'>🌱 Konsultan Hidup Sehat</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: #FFFFFF; font-weight: normal; font-size: 15px; margin-bottom: 20px; line-height: 1.4;'>Panduan Puasa Intermiten (Intermittent Fasting) sesuai Usia, Jenis Kelamin, Komposisi Tubuh, dan Riwayat Kesehatan agar Mendapatkan Autofagi yang Efektif</h5>", unsafe_allow_html=True)
    st.divider()

    # Cek Password di Secrets
    if "PASSWORD_AKSES" not in st.secrets:
        st.error("⚠️ Konfigurasi Server Belum Lengkap (Password Belum Disetting).")
        st.stop()

    # Kotak Input Password & Tombol Buka Akses
    input_pass = st.text_input("🔑 Masukkan Kode Akses Premium:", type="password", placeholder="Ketik kode akses Anda di sini...")
    tombol_akses = st.button("Buka Akses Aplikasi", type="primary", use_container_width=True)

    # LOGIKA PENGUNCIAN
    if input_pass != st.secrets["PASSWORD_AKSES"]:
        # Tampilkan error HANYA jika klien sudah mengetik sesuatu ATAU menekan tombol
        if input_pass or tombol_akses:
            if input_pass:
                st.error("⛔ Kode Akses Salah!")
            else:
                st.error("⚠️ Silakan ketik kode akses terlebih dahulu!")
        
        st.info("🔒 Aplikasi ini dikunci khusus untuk Member Premium.")
        st.markdown("""
        **Belum punya Kode Akses?**
        Dapatkan panduan pola puasa lengkap dan akses aplikasi seumur hidup dengan biaya terjangkau.
        """)
        st.link_button("🛒 Beli Kode Akses (Klik Disini)", "https://lynk.id/hahastoresby", type="primary", use_container_width=True)
        st.write("\n" * 5) 
        st.caption("Klik tombol di atas untuk mendapatkan akses.")
        st.stop()
    
    st.success("✅ Akses Diterima! Silakan isi data di bawah.")
    st.divider()

# --- JALANKAN CEK PASSWORD DULU ---
cek_password()

# =========================================================================
# AREA DI BAWAH INI HANYA AKAN MUNCUL JIKA PASSWORD BENAR
# =========================================================================

# --- FUNGSI PEMBUAT PDF (DIPERBARUI DENGAN HEADER BOX HITAM PREMIUM & SUBJUDUL) ---
def create_pdf(teks_analisa, nama_user, usia_user, logo_path="Logo_Aplikasi_Sehat.png"):
    pdf = FPDF()
    pdf.add_page()
    
    # --- 1. HEADER BOX HITAM ---
    pdf.set_fill_color(20, 20, 20)  # Warna Hitam (Almost Black)
    pdf.rect(0, 0, 210, 32, 'F')    # Lebar A4 = 210mm, Tinggi dinaikkan ke 32mm untuk subjudul
    
    # Cari lokasi logo
    if not os.path.exists(logo_path):
        if os.path.exists("../Logo_Aplikasi_Sehat.png"):
            logo_path = "../Logo_Aplikasi_Sehat.png"

    # a) LOGO DENGAN LINGKARAN PUTIH & BINGKAI EMAS
    if os.path.exists(logo_path):
        pdf.set_fill_color(218, 165, 32) # Goldenrod color
        pdf.set_draw_color(218, 165, 32)
        pdf.ellipse(9, 5, 22, 22, 'F')
        
        pdf.set_fill_color(255, 255, 255) # Putih
        pdf.ellipse(9.5, 5.5, 21, 21, 'F')
        
        pdf.image(logo_path, x=10.5, y=6.5, w=19, h=19)
    
    # b) NAMA APLIKASI (Teks Putih)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_xy(35, 6) 
    pdf.cell(0, 8, "Konsultan Hidup Sehat", ln=True)

    # c) SUBJUDUL APLIKASI
    pdf.set_font("Arial", '', 9)
    pdf.set_text_color(220, 220, 220)
    pdf.set_xy(35, 14)
    subjudul = "Panduan Puasa Intermiten (Intermittent Fasting) sesuai Usia, Jenis Kelamin, Komposisi Tubuh, dan Riwayat Kesehatan agar Mendapatkan Autofagi yang Efektif"
    pdf.multi_cell(165, 5, subjudul)
    
    pdf.set_y(35)
    
    # --- 2. HYPERLINK SUMBER ---
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(0, 0, 255)  
    pdf.cell(0, 5, "Sumber: https://aplikasisehat.streamlit.app", ln=True, align='C', link="https://aplikasisehat.streamlit.app")
    pdf.ln(2)
    
    # --- 3. NAMA KLIEN (CENTER) ---
    pdf.set_text_color(0, 0, 0) 
    pdf.set_font("Arial", 'B', 16)
    aman_nama = nama_user.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 8, f"Klien: {aman_nama} | Usia: {usia_user} Th", ln=True, align='C')
    
    # --- 4. INFO TANGGAL ANALISA (WIB) ---
    pdf.set_font("Arial", 'B', 10)
    tz_wib = timezone(timedelta(hours=7)) 
    waktu_analisa = datetime.now(tz_wib).strftime("%d-%m-%Y %H:%M WIB")
    pdf.cell(0, 5, f"Waktu Cetak: {waktu_analisa}", ln=True, align='R')
    
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y()+2, 200, pdf.get_y()+2)
