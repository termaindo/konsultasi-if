import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import base64

# --- 1. Konfigurasi Halaman ---
st.set_page_config(
    page_title="Konsultan IF & Autofagi",
    page_icon="🌱",
    layout="centered"
)

# --- FUNGSI PEMBUAT PDF ---
def create_pdf(teks_analisa, nama_user, usia_user):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Hasil Analisa Konsultan IF", ln=1, align='C')
    
    # Info User
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Klien: {nama_user} | Usia: {usia_user} Th", ln=1, align='C')
    pdf.ln(10)
    
    # Isi Analisa
    pdf.set_font("Arial", size=11)
    
    # Bersihkan karakter emoji agar PDF aman
    teks_bersih = teks_analisa.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, teks_bersih)
    
    # Footer Promosi di PDF
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, "Dapatkan panduan lengkap di Ebook 'Puasa Pintar'", ln=1, align='C')
    
    return pdf.output(dest="S").encode("latin-1")

# --- 2. Judul & Header ---
st.title("🌱 Konsultan Intermittent Fasting")
st.markdown("Dapatkan jadwal puasa, saran nutrisi **Spirulina**, dan strategi **Autofagi** sesuai kondisi tubuh Anda.")
st.divider()

# --- 3. Cek API Key ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("⚠️ API Key belum dipasang. Cek Secrets.")
    st.stop()

# --- 4. Formulir Utama ---
with st.form("form_konsultasi"):
    
    st.subheader("1️⃣ Data Fisik")
    nama = st.text_input("Nama Panggilan", "Sobat Sehat")
    
    col1, col2 = st.columns(2)
    with col1:
        usia = st.number_input("Usia (Tahun)", 15, 100, 61)
        berat = st.number_input("Berat (kg)", 30.0, 150.0, 70.0)
    with col2:
        gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        tinggi = st.number_input("Tinggi (cm)", 100.0, 250.0, 170.0)

    bmi = berat / ((tinggi/100)**2)

    st.subheader("2️⃣ Riwayat Kesehatan")
    kondisi = st.text_area("Kondisi Kesehatan:", "Sehat, tidak ada keluhan serius.", height=70)

    st.subheader("3️⃣ Pertanyaan Anda")
    pertanyaan = st.text_area("Keluhan/Pertanyaan:", "Bagaimana cara mulai puasa yang aman?", height=100)

    # REVISI: Mengganti kata Resep menjadi Panduan
    tombol = st.form_submit_button("🩺 Analisa & Berikan Panduan", type="primary", use_container_width=True)

# --- 5. Logika AI & Hasil ---
if tombol:
    # Indikator BMI
    st.divider()
    if bmi < 18.5:
        st.warning(f"⚠️ BMI: {bmi:.2f} (Underweight)")
    elif 18.5 <= bmi < 25:
        st.success(f"✅ BMI: {bmi:.2f} (Normal)")
    elif 25 <= bmi < 30:
        st.warning(f"⚠️ BMI: {bmi:.2f} (Overweight)")
    else:
        st.error(f"🚨 BMI: {bmi:.2f} (Obesity)")
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-flash-latest')
        
        prompt_sistem = f"""
        Anda adalah Ahli Krononutrisi & Praktisi Kesehatan Holistik.
        DATA USER: Nama {nama}, Usia {usia}, Gender {gender}, BMI {bmi:.2f}, Kondisi {kondisi}.
        PERTANYAAN: "{pertanyaan}"
        
        TUGAS UTAMA:
        1. Jawab pertanyaan user dengan ramah dan ilmiah.
        2. Sesuaikan jadwal puasa dengan kondisi user.
        
        TUGAS WAJIB (PRODUK & KEAMANAN):
        1. ANALISA DULU: Cek apakah user memiliki riwayat Gagal Ginjal (GGK/CKD), Asam Urat Akut, atau Autoimun tertentu yang sensitif.
           - JIKA AMAN: WAJIB sertakan paragraf khusus tentang manfaat **SPIRULINA** (Superfood) yang relevan dengan keluhan mereka (misal: untuk energi, diabetes, atau kolesterol). Sarankan sebagai suplemen alami.
           - JIKA TIDAK AMAN (ada GGK/Ginjal Berat): JANGAN sarankan Spirulina. Fokuskan saran pada diet rendah protein/kalium yang ketat dan konsultasi dokter.
        
        2. DI AKHIR SARAN (Untuk Semua User):
           Rekomendasikan membaca Ebook **"Puasa Pintar"** untuk memahami dasar ilmiah Autofagi agar puasa lebih efektif.
        
        FORMAT: 
        - Gunakan poin-poin (*) agar rapi. 
        - Hindari emoji berlebihan. 
        - Gunakan kata 'Panduan', JANGAN 'Resep'.
        """
        
        with st.spinner('Sedang menyusun panduan kesehatan Anda...'):
            response = model.generate_content(prompt_sistem)
            
            # REVISI: Judul Hasil
            st.markdown("### 💡 Panduan & Analisa Personal")
            st.markdown(response.text)
            
            st.divider()
            
            # --- BAGIAN PROMOSI EBOOK ---
            st.success("📘 **PANDUAN LENGKAP TERSEDIA**")
            col_promo, col_btn = st.columns([2, 1])
            
            with col_promo:
                st.markdown("""
                Ingin memahami sains di balik **Autofagi** dan **Penyembuhan Sel** secara utuh?
                Baca Ebook **"Puasa Pintar"**. Penjelasan ringkas, ilmiah, dan mudah dipraktikkan.
                """)
            with col_btn:
                # GANTI LINK DI BAWAH INI DENGAN LINK WA BAPAK
                link_beli = "https://wa.me/6281234567890?text=Halo%20Pak%20Musa,%20saya%20mau%20beli%20Ebook%20Puasa%20Pintar"
                st.link_button("📖 Beli Ebook", link_beli, use_container_width=True)

            st.divider()

            # --- BAGIAN DOWNLOAD PDF ---
            # REVISI: Kata-kata simpan
            st.write("📥 **Simpan Panduan Ini:**")
            file_pdf = create_pdf(response.text, nama, usia)
            
            st.download_button(
                label="📄 Download PDF (Klik Disini)",
                data=file_pdf,
                # REVISI: Nama file PDF
                file_name=f"Panduan_Sehat_{nama}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

