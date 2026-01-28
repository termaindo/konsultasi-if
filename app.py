import streamlit as st
import google.generativeai as genai

# --- 1. Konfigurasi Halaman ---
st.set_page_config(
    page_title="Konsultan IF & Autofagi",
    page_icon="🌱",
    layout="wide"
)

# --- 2. Sidebar: Input Data ---
with st.sidebar:
    st.header("⚙️ Data Pengguna")
    
    # --- LOGIKA API KEY OTOMATIS (MENDETEKSI SECRETS) ---
    # Jika di Secrets ada kunci, pakai itu. Jika tidak, minta user masukkan.
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = st.text_input("🔑 Masukkan Google API Key", type="password", help="Masukkan API Key jika belum disetting di Secrets")
    
    st.divider()
    
    # --- FORMULIR YANG TADI HILANG ---
    st.subheader("Profil Biologis")
    usia = st.number_input("Usia (Tahun)", 15, 100, 61)
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    berat = st.number_input("Berat (kg)", 30.0, 150.0, 70.0)
    tinggi = st.number_input("Tinggi (cm)", 100.0, 250.0, 170.0)
    kondisi = st.text_area("Riwayat Kesehatan", "Contoh: Pasang stent jantung, Diabetes, Maag", height=100)

    # Hitung BMI
    bmi = berat / ((tinggi/100)**2)
    
    # Indikator Visual BMI
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
        st.warning("⚠️ Aplikasi belum memiliki API Key. Mohon setting di Streamlit Secrets atau masukkan manual.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt_sistem = f"""
            Anda adalah Ahli Krononutrisi & Metabolisme.
            
            DATA USER:
            - Usia: {usia} | Gender: {gender} | BMI: {bmi:.2f}
            - Kondisi: {kondisi}
            
            TUGAS:
            Jawab pertanyaan user: "{pertanyaan}"
            
            SOP KEAMANAN:
            1. Lansia (>50th): Prioritaskan massa otot & hidrasi.
            2. BMI <18.5: Larang puasa ekstrem.
            3. Jika ada penyakit (Jantung/Diabetes): Berikan disclaimer medis & saran "Gentle Fasting".
            4. Fokus pada ritme sirkadian (jam makan ideal).
            """
            
            with st.spinner('Sedang menganalisis metabolisme Anda...'):
                response = model.generate_content(prompt_sistem)
                st.markdown("### 💡 Hasil Analisa")
                st.markdown(response.text)
                st.success("Analisa selesai. Konsultasikan ke dokter untuk keputusan final.")
                
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")


