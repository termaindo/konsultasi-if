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

# --- 4. Logika AI (RADAR PENCARI MODEL) ---
if tombol:
    if not api_key:
        st.warning("⚠️ Belum ada API Key.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # --- BAGIAN PENTING: MENCARI MODEL FLASH ---
            model_terpilih = None
            daftar_semua_model = []
            
            # Ambil semua model yang bisa generate text
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    nama = m.name
                    daftar_semua_model.append(nama)
                    
                    # CARI YANG ADA KATA 'flash' (Prioritas Utama)
                    if 'flash' in nama and '1.5' in nama:
                        model_terpilih = nama
                        break 
            
            # Jika tidak ketemu Flash, cari yang ada kata 'pro' tapi bukan 2.5 (karena berbayar)
            if not model_terpilih:
                for nama in daftar_semua_model:
                    if 'pro' in nama and 'latest' not in nama and '2.5' not in nama:
                        model_terpilih = nama
                        break

            # Kalau masih tidak ketemu, ambil sembarang yang pertama
            if not model_terpilih and daftar_semua_model:
                model_terpilih = daftar_semua_model[0]

            # --- EKSEKUSI ---
            if model_terpilih:
                # Tampilkan model apa yang dipakai (untuk info debug)
                st.caption(f"🤖 Menggunakan Otak AI: `{model_terpilih}`")
                
                model = genai.GenerativeModel(model_terpilih)
                
                prompt_sistem = f"""
                Anda adalah Ahli Krononutrisi & Metabolisme (Intermittent Fasting Expert).
                DATA USER: Usia {usia}, Gender {gender}, BMI {bmi:.2f}, Kondisi {kondisi}.
                PERTANYAAN: "{pertanyaan}"
                Jawab dengan aman, ilmiah, dan sesuaikan dengan kondisi user.
                """
                
                with st.spinner('Sedang menganalisis...'):
                    response = model.generate_content(prompt_sistem)
                    st.markdown("### 💡 Hasil Analisa")
                    st.markdown(response.text)
            else:
                st.error("Gawat! Tidak ditemukan satu pun model AI di akun ini.")
                st.write("Daftar model yang terdeteksi:", daftar_semua_model)
                
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
            # Tampilkan daftar model untuk diagnosa jika error
            st.write("Coba cek daftar model yang tersedia bagi kunci Anda:", daftar_semua_model if 'daftar_semua_model' in locals() else "Gagal memuat list")
