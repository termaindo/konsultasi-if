import streamlit as st
import google.generativeai as genai

# --- 1. Konfigurasi Halaman ---
st.set_page_config(
    page_title="Konsultan IF & Autofagi",
    page_icon="🌱",
    layout="wide"
)

# --- 2. Sidebar ---
with st.sidebar:
    st.header("⚙️ Data Pengguna")
    
    # Ambil API Key dari Secrets
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
        st.warning("⚠️ Belum ada API Key. Cek Secrets.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # --- PERBAIKAN: MENGGUNAKAN NAMA ALIAS DARI DAFTAR BAPAK ---
            # Kita pakai 'models/gemini-flash-latest' karena ini yang muncul di list Bapak (No. 16)
            nama_model = 'models/gemini-flash-latest'
            
            model = genai.GenerativeModel(nama_model)
            
            prompt_sistem = f"""
            Anda adalah Ahli Krononutrisi & Metabolisme.
            DATA USER: Usia {usia}, Gender {gender}, BMI {bmi:.2f}, Kondisi {kondisi}.
            PERTANYAAN: "{pertanyaan}"
            Jawab dengan aman, ilmiah, dan sesuaikan dengan kondisi user.
            """
            
            with st.spinner('Sedang menganalisis...'):
                response = model.generate_content(prompt_sistem)
                st.markdown("### 💡 Hasil Analisa")
                st.markdown(response.text)
                st.caption(f"Menggunakan model: {nama_model}")
                
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
