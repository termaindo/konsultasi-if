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
    
    # Judul Awal & Subjudul (Diperbarui dengan font lebih kecil dan warna putih kontras)
    st.markdown("<h1 style='text-align: center; margin-top: -10px;'>🌱 Konsultan Hidup Sehat</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: #FFFFFF; font-weight: normal; font-size: 15px; margin-bottom: 20px; line-height: 1.4;'>Panduan Puasa Intermiten (Intermittent Fasting) sesuai Usia, Jenis Kelamin, Komposisi Tubuh, dan Riwayat Kesehatan agar Mendapatkan Autofagi yang Efektif</h5>", unsafe_allow_html=True)
    st.divider()

    # Cek Password di Secrets
    if "PASSWORD_AKSES" not in st.secrets:
        st.error("⚠️ Konfigurasi Server Belum Lengkap (Password Belum Disetting).")
        st.stop()

    # Kotak Input Password
    input_pass = st.text_input("🔑 Masukkan Kode Akses Premium:", type="password", placeholder="Ketik kode akses Anda di sini...")

    # LOGIKA PENGUNCIAN
    if input_pass != st.secrets["PASSWORD_AKSES"]:
        if input_pass:
            st.error("⛔ Kode Akses Salah!")
        
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
        # Bingkai Lingkaran Emas Luar (Posisi Y disesuaikan agar di tengah box)
        pdf.set_fill_color(218, 165, 32) # Goldenrod color
        pdf.set_draw_color(218, 165, 32)
        pdf.ellipse(9, 5, 22, 22, 'F')
        
        # Latar Lingkaran Putih Dalam
        pdf.set_fill_color(255, 255, 255) # Putih
        pdf.ellipse(9.5, 5.5, 21, 21, 'F')
        
        # Cetak Gambar Logo di Atas Lingkaran Putih
        pdf.image(logo_path, x=10.5, y=6.5, w=19, h=19)
    
    # b) NAMA APLIKASI (Teks Putih)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_xy(35, 6) 
    pdf.cell(0, 8, "Konsultan Hidup Sehat", ln=True)

    # c) SUBJUDUL APLIKASI (Warna abu keputihan, font lebih kecil)
    pdf.set_font("Arial", '', 9)
    pdf.set_text_color(220, 220, 220)
    pdf.set_xy(35, 14)
    subjudul = "Panduan Puasa Intermiten (Intermittent Fasting) sesuai Usia, Jenis Kelamin, Komposisi Tubuh, dan Riwayat Kesehatan agar Mendapatkan Autofagi yang Efektif"
    pdf.multi_cell(165, 5, subjudul)
    
    # Reset posisi Y ke bawah kotak hitam
    pdf.set_y(35)
    
    # --- 2. HYPERLINK SUMBER ---
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(0, 0, 255)  # Warna Biru
    pdf.cell(0, 5, "Sumber: https://aplikasisehat.streamlit.app", ln=True, align='C', link="https://aplikasisehat.streamlit.app")
    pdf.ln(2)
    
    # --- 3. NAMA KLIEN (CENTER) ---
    pdf.set_text_color(0, 0, 0) # Kembali ke Hitam
    pdf.set_font("Arial", 'B', 16)
    aman_nama = nama_user.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 8, f"Klien: {aman_nama} | Usia: {usia_user} Th", ln=True, align='C')
    
    # --- 4. INFO TANGGAL ANALISA (DIPERBARUI KE WIB) ---
    pdf.set_font("Arial", 'B', 10)
    tz_wib = timezone(timedelta(hours=7)) # Mengatur zona waktu ke UTC+7 (WIB)
    waktu_analisa = datetime.now(tz_wib).strftime("%d-%m-%Y %H:%M WIB")
    pdf.cell(0, 5, f"Waktu Cetak: {waktu_analisa}", ln=True, align='R')
    
    # Garis Bawah Header
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y()+2, 200, pdf.get_y()+2)
    pdf.ln(5)
    
    # --- 5. BODY LAPORAN (PARSING OTOMATIS) ---
    teks_bersih = teks_analisa.encode('latin-1', 'ignore').decode('latin-1')
    
    for baris in teks_bersih.split('\n'):
        baris_pdf = baris.replace('**', '').replace('### ', '').replace('## ', '').strip()
        
        # JIKA BARIS ADALAH JUDUL BAGIAN (I, II, III, IV, V, VI, VII)
        if baris_pdf.startswith(('I.', 'II.', 'III.', 'IV.', 'V.', 'VI.', 'VII.')):
            pdf.ln(6)
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(0, 102, 204) # WARNA BIRU ELEGAN
            pdf.multi_cell(0, 7, baris_pdf)
            pdf.ln(1)
            pdf.set_text_color(0, 0, 0) # Kembalikan ke teks hitam biasa
            
        # JIKA BARIS ADALAH BULLET POINT
        elif baris_pdf.startswith('-') or baris_pdf.startswith('*'):
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, "  " + baris_pdf)
            
        # TEKS PARAGRAF BIASA
        else:
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, baris_pdf)
            
    # Footer Promosi di PDF
    pdf.ln(15)
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "Dapatkan panduan lengkap di Ebook 'Puasa Pintar'", ln=1, align='C')
    
    return pdf.output(dest="S").encode("latin-1")

# --- 3. Cek API Key ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("⚠️ API Key belum dipasang. Cek Secrets.")
    st.stop()

# --- 4. Formulir Utama ---
with st.form("form_konsultasi"):
    
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

    st.subheader("2️⃣ Riwayat Kesehatan")
    kondisi = st.text_area("Kondisi Kesehatan:", "Ceritakan kondisi kesehatan Anda yang terakhir.", height=70)

    st.subheader("3️⃣ Pertanyaan Anda")
    pertanyaan = st.text_area("Keluhan/Pertanyaan:", "Bagaimana cara mulai puasa yang aman?", height=100)

    tombol = st.form_submit_button("🩺 Analisa & Berikan Panduan", type="primary", use_container_width=True)

# --- 5. Logika AI & Hasil ---
if tombol:
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
        
        # --- PROMPT AI (DIPERBARUI DENGAN STRUKTUR 7 BAGIAN YANG PRESISI) ---
        prompt_sistem = f"""
        PERAN ANDA:
        Anda adalah Ahli Krononutrisi & Praktisi Kesehatan Holistik.
        
        DATA USER:
        Nama: {nama}
        Usia: {usia}
        Gender: {gender}
        BMI: {bmi:.2f}
        Kondisi: {kondisi}
        Pertanyaan: "{pertanyaan}"
        
        INSTRUKSI KHUSUS & FORMAT OUTPUT (IKUTI SECARA KETAT):
        
        ATURAN UMUM:
        - Tulis kepanjangan istilah teknis (IF, TRE, GERD, dll) saat pertama muncul.
        - WAJIB gunakan istilah "Pemutusan / Buka Puasa (Break the Fast)".
        - Format Judul: Gunakan Markdown (###) HANYA pada judul utama berangka Romawi (I sampai VII). 
        - DILARANG KERAS MENGGUNAKAN EMOJI PADA JUDUL agar PDF dapat dicetak sempurna dan diwarnai oleh sistem.
        - WAJIB gunakan struktur angka Romawi persis seperti urutan di bawah ini.
        
        STRUKTUR LAPORAN HARUS SEPERTI INI:
        
        (TANPA JUDUL, LANGSUNG TULISKAN SALAM)
        Salam sehat {nama}, Terima kasih atas pertanyaan Anda yang sangat proaktif. Memulai puasa, atau yang dikenal secara ilmiah sebagai *Intermittent Fasting (IF)*, adalah langkah luar biasa untuk kesehatan metabolisme dan perbaikan sel. Mengingat data dan keluhan Anda, berikut adalah panduan bertahap dan aman yang telah dirancang khusus untuk Anda.
        
        ### I. ANALISA KONDISI SAAT INI
        Berikan evaluasi singkat mengenai status BMI, Usia, dan Kondisi Kesehatan user saat ini, serta jawab secara ringkas keluhan utama mereka.
        
        ### II. PANDUAN MEMULAI PUASA AMAN BAGI PEMULA ({nama.upper()})
        Jelaskan bahwa tubuh butuh adaptasi (menghindari kejutan metabolik). Susun menjadi 3 sub-poin berikut (gunakan cetak tebal untuk nama fase):
        - **FASE PERSIAPAN (1 - 3 hari Sebelum Puasa):** Sarankan audit kebiasaan makan (kurangi gula/karbohidrat sederhana), prioritaskan kualitas tidur, dan optimalkan hidrasi.
        - **FASE IMPLEMENTASI: Metode TRE 12:12 (1 Minggu Pertama):** Instruksikan untuk puasa 12 jam (misal jam 20.00 hingga 08.00). Fokus pada membiasakan lambung istirahat.
        - **FASE PENINGKATAN: Metode TRE 14:10 sampai 16:8 (Minggu ke-2 dst):** Jelaskan cara menaikkan jam puasa perlahan setelah tubuh nyaman, agar pembakaran lemak dan autofagi mulai aktif.
        
        ### III. POLA PUASA HARIAN DALAM SEMINGGU (Weekly Daily Routine)
        - Jika Lansia/Rentan/Pemula: Beri pola KONSISTEN (misal TRE 16:8 setiap hari) agar ritme sirkadian stabil.
        - Jika Sehat/Terbiasa: Beri pola BERSELANG-SELING (*Metabolic Flexibility*) contohnya kombinasi OMAD (24 jam), TRE 16:8, dan TRE 12:12.
        - Tuliskan rincian jadwal hariannya secara jelas (Senin sampai Minggu).
        
        ### IV. SARAN OLAHRAGA & WAKTU PELAKSANAAN
        - Rekomendasi Jenis: Lansia/rentan (peregangan, beban ringan). Dewasa sehat (Kardio LISS & Beban/HIIT).
        - Rekomendasi Waktu (Timing): Kardio intensitas rendah-sedang di Jendela Puasa (*Fasted State*) untuk oksidasi lemak. Latihan Beban di Jendela Makan (*Fed State*) untuk sintesis otot.
        
        ### V. PANDUAN PEMUTUSAN / BUKA PUASA (Break the Fast)
        Jelaskan bahwa cara mengakhiri puasa sama pentingnya dengan puasanya. Hindari "Pesta" kalori. Jelaskan urutan yang benar (Mulai dari air mineral/kaldu tulang, dilanjut serat/protein ringan yang mudah dicerna, sebelum masuk ke karbohidrat kompleks).
        
        ### VI. ANALISA KELAYAKAN PUASA PANJANG & BERKALA
        - Lakukan evaluasi ketat berdasarkan parameter Usia, Gender, BMI, Kondisi.
        - Jika TIDAK AMAN (BMI < 18.5, lansia, rentan): Nyatakan dengan TEGAS bahwa Puasa Panjang (48-72 jam) TIDAK DIREKOMENDASIKAN. Beri alternatif batas aman (misal OMAD 24 jam dengan interval 1-2x seminggu).
        - Jika AMAN: Nyatakan MEMUNGKINKAN. Jelaskan tanda kesiapan (*Fat-Adapted*), Pentahapan, Interval, Manfaat (Autofagi Dr. Yoshinori Ohsumi), dan Peringatan Elektrolit.
        
        ### VII. REKOMENDASI NUTRISI PENDAMPING
        - Jika user memiliki sakit Ginjal/Asam Urat/Alergi Seafood: JANGAN sebut kata "Spirulina". Bahas asupan alami (Real Food) utuh.
        - Jika AMAN: Jelaskan kehebatan Spirulina (Energi seluler, detoksifikasi). 
        - JIKA AMAN, WAJIB tutup bagian VII ini dengan kalimat persis: "Silakan cek rekomendasi nutrisi di bawah ini."
        """
        
        with st.spinner('Sedang menyusun panduan kesehatan & analisa puasa panjang Anda...'):
            response = model.generate_content(prompt_sistem)
            
            st.markdown("### 💡 Laporan & Analisa Personal")
            st.markdown(response.text)
            st.divider()
            
            # --- LOGIKA PYTHON SPIRULINA ---
            kata_bahaya = ["ginjal", "gagal", "cuci darah", "ckd", "hemo", "kreatinin", "asam urat", "alergi seafood"]
            is_spirulina_aman = True
            
            for kata in kata_bahaya:
                if kata in kondisi.lower():
                    is_spirulina_aman = False
                    break
            
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
                    link_spirulina = "https://wa.me/6281801016090?text=Halo%20kak%20Elisa,%20saya%20tertarik%20pesan%20Spirulina%20Rekomendasi%20Aplikasi%20Sehat."
                    st.link_button("🛒 Order Spirulina", link_spirulina, use_container_width=True)
                st.divider()
            
            # --- BAGIAN EBOOK ---
            st.success("📘 **PANDUAN LENGKAP TERSEDIA**")
            col_promo, col_btn = st.columns([2, 1])
            with col_promo:
                st.markdown("""
                Pahami sains **Autofagi & Penyembuhan Sel** secara utuh.
                Baca Ebook **"Puasa Pintar"**. Ringkas, ilmiah, mudah dipraktikkan.
                """)
            with col_btn:
                link_ebook = "https://wa.me/6281802026090?text=Halo%20kak%20Elisa,%20saya%20mau%20beli%20Ebook%20Puasa%20Pintar%yang%20direkomendasikan%20Aplikasi%20Sehat."
                st.link_button("📖 Order Ebook", link_ebook, use_container_width=True)

            st.divider()

            # --- DOWNLOAD PDF ---
            st.write("📥 **Simpan Panduan Ini:**")
            file_pdf = create_pdf(response.text, nama, usia)
            
            st.download_button(
                label="📄 Download Laporan PDF (Klik Disini)",
                data=file_pdf,
                file_name=f"Panduan_Sehat_{nama}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
            # PADDING BAWAH (UNTUK HALAMAN HASIL)
            st.write("\n" * 5)
            
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
