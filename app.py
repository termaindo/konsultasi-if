import streamlit as st
import google.generativeai as genai
import time

# --- 1. Konfigurasi Halaman ---
st.set_page_config(
    page_title="Konsultan IF & Autofagi",
    page_icon="🌱",
    layout="wide"
)

# --- 2. Sidebar ---
with st.sidebar:
    st.header("⚙️ Data Pengguna")
    
    # Ambil API Key dari Secrets (Brankas)
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = st.text_input("🔑 Masukkan Google API Key", type="password")
    
    st.divider()
    
    # Formulir
    st.subheader("Profil Biologis")
    usia = st.number_input("Usia (Tahun)", 15, 100, 61)
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    berat = st.number_input("Berat (kg)", 30.0, 150.0, 70.0)
    tinggi = st.number_input("Tinggi (cm)", 100.0, 250.0, 170.0)
    kondisi = st.text_area("Riwayat Kesehatan", "Contoh: Pasang stent jantung, Diabetes, Maag", height=100)

    # Hitung BMI
    bmi = berat / ((tinggi/100)**2)
    
    if bmi < 18.5:
        st.warning(f"⚠️ BMI: {bmi:.2f} (Underweight)")
    elif 18.5 <= bmi < 25:
        st.success(f"✅ BMI: {bmi:.2f} (Normal)")
    elif 25 <= bmi < 30:
        st.warning(f"⚠️ BMI: {bmi:.2f} (Overweight)")
    else:
        st.error(f"🚨 BMI: {bmi:.2f} (Obesity)")

# --- 3. Area Utama ---
st.title("🌱 Konsultan Intermittent Fasting & Autofagi")
st.markdown("Dapatkan panduan puasa yang **aman** dan disesuaikan dengan kondisi medis Anda.")

pertanyaan = st.text_area("Apa yang ingin Anda tanyakan?", height=100, placeholder="Misal: Saya punya maag, jam berapa sebaiknya mulai puasa?")
tombol = st.button("Analisa Profil & Jawab", type="primary")

# --- 4. Logika AI ---
if tombol:
    if not api_key:
        st.warning("⚠️ Belum ada API Key. Mohon cek setting Secrets.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # --- MODEL FINAL: GEMINI 1.5 FLASH ---
            # Model ini kuota gratisnya 15 RPM (Request Per Minute). Sangat cukup.
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt_sistem = f"""
            Anda adalah Ahli Krononutrisi & Metabolisme (Intermittent Fasting Expert).
            
            DATA USER:
            - Usia: {usia} Tahun | Gender: {gender}
            - BMI: {bmi:.2f} | Kondisi: {kondisi}
            
            PERTANYAAN: "{pertanyaan}"
            
            SOP:
            1. Sesuaikan saran dengan Usia Lanjut (>50) & BMI.
            2. Wajib Disclaimer Medis.
            3. Fokus Autofagi & Sirkadian.
            """
            
            with st.spinner('Sedang menganalisis...'):
                response = model.generate_content(prompt_sistem)
                st.markdown("### 💡 Hasil Analisa")
                st.markdown(response.text)
                
        except Exception as e:
            # Jika masih error, kita tampilkan pesan yang jelas
            err_msg = str(e)
            if "429" in err_msg:
                st.error("⏳ Terlalu banyak permintaan. Mohon tunggu 1 menit.")
            elif "404" in err_msg:
                st.error("⚠️ Masalah Versi. Mohon lakukan REBOOT App di menu Manage App.")
            else:
                st.error(f"Terjadi kesalahan: {err_msg}")
