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
    
    # Cek API Key
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

# --- 4. Logika AI (Versi Stabil & Gratis) ---
if tombol:
    if not api_key:
        st.warning("⚠️ Belum ada API Key.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # KITA KUNCI KE MODEL YANG PASTI GRATIS & STABIL
            # Menggunakan Gemini 1.5 Flash
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt_sistem = f"""
            Anda adalah Ahli Krononutrisi & Metabolisme (Intermittent Fasting Expert).
            
            DATA USER:
            - Usia: {usia} Tahun
            - Gender: {gender}
            - BMI: {bmi:.2f}
            - Kondisi Medis: {kondisi}
            
            PERTANYAAN USER: "{pertanyaan}"
            
            TUGAS:
            Jawablah dengan gaya bahasa dokter yang ramah namun tegas.
            
            SOP KEAMANAN (WAJIB):
            1. Jika Usia > 50: Ingatkan risiko kehilangan otot (sarkopenia) & pentingnya protein.
            2. Jika BMI < 18.5: Larang puasa panjang (>14 jam).
            3. Jika ada Riwayat Jantung/Stent/Diabetes:
               - Wajib sertakan DISCLAIMER bahwa ini edukasi, bukan resep dokter.
               - Sarankan konsultasi dokter jantung/internis.
               - Fokuskan manfaat autofagi untuk pemulihan sel, tapi ingatkan bahaya dehidrasi.
            4. Berikan saran Jam Makan yang sesuai irama sirkadian (Matahari).
            """
            
            with st.spinner('Sedang menganalisis metabolisme Anda...'):
                response = model.generate_content(prompt_sistem)
                st.markdown("### 💡 Hasil Analisa")
                st.markdown(response.text)
                st.info("ℹ️ Tips: Minum air putih yang cukup saat jendela puasa.")
                
        except Exception as e:
            # Penanganan Error yang Lebih Manusiawi
            error_msg = str(e)
            if "429" in error_msg:
                st.error("⏳ Server sedang sibuk (Kuota Gratis Penuh). Mohon tunggu 1 menit lalu coba lagi.")
            elif "404" in error_msg:
                st.error("⚠️ Model sedang maintenance. Silakan coba refresh halaman.")
            else:
                st.error(f"Terjadi kesalahan: {error_msg}")
