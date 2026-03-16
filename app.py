import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import base64
import os
import json
from datetime import datetime, timedelta, timezone

# --- 1. Konfigurasi Halaman ---
st.set_page_config(
    page_title="Konsultan Hidup Sehat",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed" # Memastikan sidebar tertutup dari awal
)

# --- SCRIPT PENGHILANG MENU, SIDEBAR, & CSS ---
hide_menu_style = """
<style>
/* 1. Sembunyikan Header & Menu Utama */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* 2. MATIKAN SIDEBAR SECARA TOTAL UNTUK HP */
[data-testid="collapsedControl"] {display: none !important;}
[data-testid="stSidebar"] {display: none !important;}
section[data-testid="stSidebar"] {display: none !important;}

/* 3. Sembunyikan Tombol Floating */
[data-testid="stToolbar"] {display: none !important;}
[data-testid="stDecoration"] {display: none !important;}
[data-testid="stStatusWidget"] {display: none !important;}
div[class*="viewerBadge"] {display: none !important;}

/* 4. MANUVER JARAK AMAN (PADDING BAWAH) */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 150px !important; 
}

/* 5. PERCANTIK TAMPILAN HEADER DI WEB */
h3 {
    color: #0066cc;
    border-bottom: 2px solid #f0f2f6;
    padding-bottom: 5px;
    margin-top: 25px;
}
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
        st.error("⚠️ Konfigurasi Server Belum Lengkap (Password Belum Disetting).")
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

# --- JALANKAN CEK PASSWORD DULU ---
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
# NAVIGASI MENU (IN-PAGE NAVIGATION SANGAT COCOK UNTUK HP)
# =========================================================================
st.markdown("### 🧭 Menu Utama")
menu_app = st.selectbox(
    "Silakan pilih modul yang ingin dibuka:",
    ["1️⃣ Profil & Panduan Puasa (IF)", "2️⃣ Modul Nutrisi & Superfood", "3️⃣ Modul Olahraga"]
)
st.divider()

# =========================================================================
# MODUL 1: PROFIL & PUASA
# =========================================================================
if menu_app == "1️⃣ Profil & Panduan Puasa (IF)":
    st.markdown("### 📝 Data Diri")

    st.subheader("1️⃣ Data Fisik")
    nama = st.text_input("Nama Panggilan", "Sobat Sehat")

    col1, col2 = st.columns(2)
    with col1:
        usia = st.number_input("Usia (Tahun)", 15, 100, 41)
        berat = st.number_input("Berat (kg)", 30.0, 150.0, 70.0)
    with col2:
        gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        tinggi = st.number_input("Tinggi (cm)", 100.0, 250.0, 170.0)

    bmi = berat / ((tinggi/100)**2)

    st.subheader("2️⃣ Pengalaman Puasa")
    pengalaman_puasa = st.radio("Apakah Anda sudah biasa berpuasa intermiten?", ["Iya", "Baru akan mencoba", "Sudah pernah tapi sudah berhenti"])
    lama_berhenti = st.text_input("Sudah berhenti berapa lama? (dalam bulan)") if pengalaman_puasa == "Sudah pernah tapi sudah berhenti" else ""
    butuh_panduan_pemula = st.radio("Apakah Anda memerlukan Panduan Aman untuk Mulai Berpuasa bagi Pemula?", ["Iya", "Tidak"])

    st.subheader("3️⃣ Riwayat Kesehatan")
    kondisi = st.text_area("Kondisi Kesehatan:", "Ceritakan kondisi kesehatan Anda yang terakhir.", height=70)

    st.subheader("4️⃣ Pertanyaan Anda")
    pertanyaan = st.text_area("Keluhan/Pertanyaan:", "Bagaimana cara mulai puasa yang aman?", height=100)

    tombol = st.button("🩺 Analisa & Susun Puasa", type="primary", use_container_width=True)

    if tombol:
        # SIMPAN KE KOPER DIGITAL
        st.session_state['user_profile'] = {
            "nama": nama, "usia": usia, "gender": gender, "tinggi": tinggi, "berat": berat,
            "bmi": bmi, "kondisi": kondisi, "pertanyaan": pertanyaan
        }

        st.divider()
        if bmi < 18.5: st.warning(f"⚠️ BMI: {bmi:.2f} (Underweight)")
        elif 18.5 <= bmi < 25: st.success(f"✅ BMI: {bmi:.2f} (Normal)")
        elif 25 <= bmi < 30: st.warning(f"⚠️ BMI: {bmi:.2f} (Overweight)")
        else: st.error(f"🚨 BMI: {bmi:.2f} (Obesity)")
            
        try:
            teks_berhenti = f" (Telah berhenti {lama_berhenti} bulan)" if lama_berhenti else ""
            
            prompt_sistem = f"""
            PERAN: Ahli Krononutrisi & Praktisi Kesehatan Holistik.
            DATA USER: Nama: {nama}, Usia: {usia}, Gender: {gender}, BMI: {bmi:.2f}, Pengalaman: {pengalaman_puasa}{teks_berhenti}, Butuh Pemula: {butuh_panduan_pemula}, Kondisi: {kondisi}, Tanya: {pertanyaan}.
            
            FORMAT (Tanpa Judul Besar, Gunakan Markdown ### untuk Angka Romawi):
            Salam sehat {nama}, ... (kalimat pembuka).
            
            ### I. ANALISA KONDISI SAAT INI
            (Isi evaluasi singkat)
            """

            if butuh_panduan_pemula == "Iya":
                prompt_sistem += f"""
            ### II. PANDUAN MEMULAI PUASA AMAN BAGI PEMULA
            (Fase Persiapan, Implementasi 12:12, Peningkatan 14:10/16:8)
            ### III. POLA PUASA HARIAN DALAM SEMINGGU
            (Jadwal harian Senin-Minggu)
            ### IV. PANDUAN PEMUTUSAN / BUKA PUASA
            (Urutan berbuka yang aman)
            ### V. ANALISA KELAYAKAN PUASA PANJANG
            (Aman atau tidaknya 48-72 jam)
            """
            else:
                prompt_sistem += f"""
            ### II. POLA PUASA HARIAN DALAM SEMINGGU
            (Jadwal harian Senin-Minggu lanjutan/berselang-seling)
            ### III. PANDUAN PEMUTUSAN / BUKA PUASA
            (Urutan berbuka yang aman)
            ### IV. ANALISA KELAYAKAN PUASA PANJANG
            (Aman atau tidaknya 48-72 jam)
            """

            prompt_sistem += "\n### PENTING: Untuk rekomendasi Olahraga dan Menu Makan, silakan buka Modul Nutrisi & Olahraga di menu Navigasi Atas."

            with st.spinner('Sedang menyusun jadwal puasa Anda...'):
                response = model.generate_content(prompt_sistem)
                st.markdown("### 💡 Laporan Pola Puasa")
                st.markdown(response.text)
                
                st.success("👇 **Langkah Selanjutnya:** Gulir ke atas, pada kotak **Menu Utama**, ganti pilihan ke **Modul Nutrisi & Superfood** untuk melihat menu makan Anda.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")


# =========================================================================
# MODUL 2: NUTRISI & SUPERFOOD
# =========================================================================
elif menu_app == "2️⃣ Modul Nutrisi & Superfood":
    st.markdown("### 🥗 Modul Nutrisi Khusus")
    
    if 'user_profile' not in st.session_state:
        st.warning("⚠️ Silakan isi data diri Anda di menu **1️⃣ Profil & Panduan Puasa** terlebih dahulu.")
    else:
        data = st.session_state['user_profile']
        st.info(f"Profil aktif: **{data['nama']}** | Usia: **{data['usia']} th** | BMI: **{data['bmi']:.2f}**")
        
        alergi = st.text_input("Apakah Anda memiliki Alergi Makanan tertentu?", placeholder="Contoh: Kacang, Telur, Seafood. Kosongkan jika tidak ada.")
        
        if st.button("🍎 Susun Pola Nutrisi Saya", type="primary", use_container_width=True):
            prompt_nutrisi = f"""
            TUGAS: Susun nutrisi jendela makan dengan format JSON.
            DATA UMUM: Usia {data['usia']}, BMI {data['bmi']:.2f}, Kondisi: {data['kondisi']}.
            ALERGI: {alergi if alergi else 'Tidak ada'}.
            
            ATURAN JSON:
            {{
              "keamanan": "Teks penjelasan mengapa menu ini aman untuk kondisinya dan alerginya.",
              "menu": {{
                "berbuka": {{"nama": "teks", "alasan": "teks"}},
                "utama": {{"nama": "teks", "alasan": "teks"}},
                "penutup": {{"nama": "teks", "alasan": "teks"}}
              }}
            }}
            """
            
            with st.spinner("Meracik menu yang aman untuk Anda..."):
                resp_nutrisi = model.generate_content(prompt_nutrisi)
                json_data = parse_ai_json(resp_nutrisi.text)
                
                if json_data:
                    st.success("✅ Menu Nutrisi Berhasil Disusun!")
                    st.write(f"**🛡️ Catatan Ahli:** {json_data['keamanan']}")
                    
                    st.markdown(f"**🌅 Saat Berbuka:** {json_data['menu']['berbuka']['nama']}")
                    st.caption(f"*Alasan:* {json_data['menu']['berbuka']['alasan']}")
                    
                    st.markdown(f"**🍽️ Makan Utama:** {json_data['menu']['utama']['nama']}")
                    st.caption(f"*Alasan:* {json_data['menu']['utama']['alasan']}")
                    
                    st.markdown(f"**🌙 Sebelum Puasa:** {json_data['menu']['penutup']['nama']}")
                    st.caption(f"*Alasan:* {json_data['menu']['penutup']['alasan']}")
                    
                    st.divider()
                    
                    # LOGIKA SPIRULINA
                    kata_bahaya = ["ginjal", "gagal", "cuci darah", "ckd", "hemo", "kreatinin", "asam urat", "alergi seafood"]
                    is_spirulina_aman = not any(k in data['kondisi'].lower() for k in kata_bahaya)
                    
                    if is_spirulina_aman:
                        st.info("🌿 **SUPERFOOD PENDAMPING: SPIRULINA**")
                        st.markdown("Spirulina Grade A disarankan untuk memenuhi mikronutrisi Anda saat jendela makan. Sangat baik untuk energi & detoks seluler.")
                        link_sp = "https://wa.me/6281801016090?text=Halo%20kak%20Elisa,%20saya%20tertarik%20pesan%20Spirulina."
                        st.link_button("🛒 Order Spirulina", link_sp, use_container_width=True)
                else:
                    st.error("Gagal menyusun menu. Silakan klik tombol susun kembali.")


# =========================================================================
# MODUL 3: OLAHRAGA
# =========================================================================
elif menu_app == "3️⃣ Modul Olahraga":
    st.markdown("### 🏃 Modul Olahraga Pintar")
    
    if 'user_profile' not in st.session_state:
        st.warning("⚠️ Silakan isi data diri Anda di menu **1️⃣ Profil & Panduan Puasa** terlebih dahulu.")
    else:
        data = st.session_state['user_profile']
        st.info(f"Profil aktif: **{data['nama']}** | Usia: **{data['usia']} th**")
        
        if st.button("💪 Susun Pola Olahraga Saya", type="primary", use_container_width=True):
            prompt_olga = f"""
            TUGAS: Buatkan saran jadwal olahraga format JSON.
            DATA: Usia {data['usia']}, BMI {data['bmi']:.2f}, Kondisi: {data['kondisi']}.
            
            ATURAN JSON:
            {{
              "peringatan_medis": "Teks peringatan batas aman (contoh: awas lutut karena BMI tinggi).",
              "latihan_jendela_puasa": "Saran kardio ringan",
              "latihan_jendela_makan": "Saran latihan beban/pembentukan otot",
              "target_detak_jantung": "Angka/teks batasan"
            }}
            """
            with st.spinner("Mendesain program latihan Anda..."):
                resp_olga = model.generate_content(prompt_olga)
                json_olga = parse_ai_json(resp_olga.text)
                
                if json_olga:
                    st.success("✅ Jadwal Olahraga Berhasil Disusun!")
                    st.error(f"**⚠️ Peringatan Keamanan:** {json_olga['peringatan_medis']}")
                    st.write(f"**🏃 Saat Sedang Berpuasa:** {json_olga['latihan_jendela_puasa']}")
                    st.write(f"**🏋️ Saat Jendela Makan:** {json_olga['latihan_jendela_makan']}")
                    st.write(f"**💓 Target Detak Jantung:** {json_olga['target_detak_jantung']}")
                else:
                    st.error("Gagal menyusun jadwal. Silakan coba lagi.")
