import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import base64

# --- 1. Konfigurasi Halaman ---
st.set_page_config(
    page_title="Konsultan Hidup Sehat",
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
    pdf.cell(200, 10, txt="Hasil Analisa Konsultan Hidup Sehat", ln=1, align='C')
    
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
st.title("🌱 Konsultan Hidup Sehat")
st.markdown("Dapatkan pola Puasa Pintar (Intermittent Fasting), saran nutrisi, dan strategi **Autofagi** sesuai kondisi tubuh Anda.")
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
        usia = st.number_input("Usia (Tahun)", 15, 100, 41)
        berat = st.number_input("Berat (kg)", 30.0, 150.0, 70.0)
    with col2:
        gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        tinggi = st.number_input("Tinggi (cm)", 100.0, 250.0, 170.0)

    bmi = berat / ((tinggi/100)**2)

    st.subheader("2️⃣ Riwayat Kesehatan")
    kondisi = st.text_area("Kondisi Kesehatan:", "Sehat, tidak ada keluhan serius.", height=70)

    st.subheader("3️⃣ Pertanyaan Anda")
    pertanyaan = st.text_area("Keluhan/Pertanyaan:", "Bagaimana cara mulai puasa yang aman?", height=100)

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
        
        # --- PROMPT AI ---
        prompt_sistem = f"""
        Anda adalah Ahli Krononutrisi & Praktisi Kesehatan Holistik.
        DATA USER: Nama {nama}, Usia {usia}, Gender {gender}, BMI {bmi:.2f}, Kondisi {kondisi}.
        PERTANYAAN: "{pertanyaan}"
        
        TUGAS UTAMA:
        1. Jawab pertanyaan user dengan ramah dan ilmiah.
        2. Sesuaikan jadwal puasa dengan kondisi user.
        
        ATURAN PENULISAN (PENTING):
        - Jika menggunakan istilah teknis/singkatan (IF, TRE, CKD, GGK, dll), WAJIB tuliskan kepanjangannya saat pertama disebut.
        
        LOGIKA PROMOSI PRODUK (BRAND PROTECTION PROTOCOL):
        Lakukan screening ketat terhadap kondisi user:
        
        1. CEK KONTRAINDIKASI: Apakah user memiliki riwayat Gagal Ginjal (GGK/CKD/Cuci Darah), Asam Urat Akut berat, Alergi Seafood Berat, atau Autoimun sensitif?
           - JIKA BAHAYA: Gunakan kalimat samar: "Kami tidak merekomendasikan suplemen pekat/tinggi protein." (Jangan sebut merk).
           - JIKA AMAN: WAJIB jelaskan manfaat **SPIRULINA** (Superfood) sesuai keluhan user. 
             Akhiri paragraf Spirulina dengan kalimat: "Silakan cek rekomendasi nutrisi di bawah ini."
        
        2. PROMOSI EBOOK:
           Di akhir, rekomendasikan Ebook **"Puasa Pintar"**.
        
        FORMAT: Gunakan poin-poin (*), hindari emoji berlebihan, gunakan kata 'Panduan'.
        """
        
        with st.spinner('Sedang menyusun panduan kesehatan Anda...'):
            response = model.generate_content(prompt_sistem)
            
            # Tampilkan Hasil Analisa
            st.markdown("### 💡 Panduan & Analisa Personal")
            st.markdown(response.text)
            
            st.divider()
            
            # --- LOGIKA PYTHON UNTUK MENAMPILKAN PROMO SPIRULINA (UPSELLING CERDAS) ---
            # Kita filter manual di Python agar tombol benar-benar hilang jika user berisiko
            kata_bahaya = ["ginjal", "gagal", "cuci darah", "ckd", "hemo", "kreatinin", "asam urat", "alergi seafood"]
            is_spirulina_aman = True
            
            # Cek apakah ada kata bahaya di kondisi user
            for kata in kata_bahaya:
                if kata in kondisi.lower():
                    is_spirulina_aman = False
                    break
            
            # JIKA AMAN, TAMPILKAN KOTAK PROMO SPIRULINA
            if is_spirulina_aman:
                st.info("🌿 **NUTRISI PENDAMPING (SUPERFOOD)**")
                col_sp1, col_sp2 = st.columns([3, 1])
                with col_sp1:
                    st.markdown("""
                    Berdasarkan profil Anda, **Spirulina** disarankan untuk:
                    * Memenuhi kebutuhan mikronutrisi saat jendela makan.
                    * Meningkatkan energi & detoksifikasi seluler alami.
                    Untuk itu, kami sudah bantu kurasikan Spirulina khusus Grade A, yaitu yang Food Grade untuk manusia, bukan Spirulina yang hanya bisa dipakai sebagai Masker Wajah, atau Spirulina sebagai bahan campuran pakan ternak.
                    """)
                with col_sp2:
                    # GANTI NO WA DI SINI (PESAN SPIRULINA)
                    link_spirulina = "https://wa.me/6281801016090?text=Halo%20kak%20Elisa,%20saya%20tertarik%20pesan%20Spirulina%20Rekomendasi%20Aplikasi%20Sehat."
                    st.link_button("🛒 Order Spirulina", link_spirulina, use_container_width=True)
                st.divider()
            
            # --- BAGIAN PROMOSI EBOOK (SELALU MUNCUL) ---
            st.success("📘 **PANDUAN LENGKAP TERSEDIA**")
            col_promo, col_btn = st.columns([2, 1])
            with col_promo:
                st.markdown("""
                Pahami sains **Autofagi & Penyembuhan Sel** secara utuh.
                Baca Ebook **"Puasa Pintar"**. Ringkas, ilmiah, mudah dipraktikkan.
                """)
            with col_btn:
                # GANTI NO WA DI SINI (PESAN EBOOK)
                link_ebook = "https://wa.me/6281802026090?text=Halo%20kak%20Elisa,%20saya%20mau%20beli%20Ebook%20Puasa%20Pintar%yang%20direkomendasikan%20Aplikasi%20Sehat."
                st.link_button("📖 Order Ebook", link_ebook, use_container_width=True)

            st.divider()

            # --- DOWNLOAD PDF ---
            st.write("📥 **Simpan Panduan Ini:**")
            file_pdf = create_pdf(response.text, nama, usia)
            
            st.download_button(
                label="📄 Download PDF (Klik Disini)",
                data=file_pdf,
                file_name=f"Panduan_Sehat_{nama}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
