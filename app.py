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
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# --- 2. FUNGSI GATEKEEPER (GERBANG TOL) ---
def cek_password():
    """Fungsi untuk memblokir akses jika password salah"""
    
    # Judul Awal
    st.title("🌱 Konsultan Hidup Sehat")
    st.write("Selamat datang di Aplikasi Panduan Puasa Intermiten (Intermittent Fasting)"
             "sesuai Usia, Jenis Kelamin, BMI, dan Riwayat Kesehatan"
             "agar Mencapai Autofagi yang Efektif.")
    st.divider()

    # Cek Password di Secrets
    if "PASSWORD_AKSES" not in st.secrets:
        st.error("⚠️ Konfigurasi Server Belum Lengkap (Password Belum Disetting).")
        st.stop()

    # Kotak Input Password
    input_pass = st.text_input("🔑 Masukkan Kode Akses Premium:", type="password", placeholder="Ketik kode akses Anda di sini...")

    # LOGIKA PENGUNCIAN
    if input_pass != st.secrets["PASSWORD_AKSES"]:
        # Jika salah/kosong
        if input_pass:
            st.error("⛔ Kode Akses Salah!")
        
        # Pesan Info
        st.info("🔒 Aplikasi ini dikunci khusus untuk Member Premium.")
        
        st.markdown("""
        **Belum punya Kode Akses?**
        Dapatkan panduan pola puasa lengkap dan akses aplikasi seumur hidup dengan biaya terjangkau.
        """)
        
        # Tombol Link Pembelian
        st.link_button("🛒 Beli Kode Akses (Klik Disini)", "https://lynk.id/hahastoresby", type="primary", use_container_width=True)
        
        # Tambahan Spacer Manual (Jaga-jaga jika CSS gagal di browser tertentu)
        st.write("\n" * 5) 
        st.caption("Klik tombol di atas untuk mendapatkan akses.")
        
        # HENTIKAN APLIKASI
        st.stop()
    
    # JIKA BENAR
    st.success("✅ Akses Diterima! Silakan isi data di bawah.")
    st.divider()

# --- JALANKAN CEK PASSWORD DULU ---
cek_password()

# =========================================================================
# AREA DI BAWAH INI HANYA AKAN MUNCUL JIKA PASSWORD BENAR
# =========================================================================

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
    
    # Bersihkan karakter emoji
    teks_bersih = teks_analisa.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, teks_bersih)
    
    # Footer PDF
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
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
        
        # --- PROMPT AI ---
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
        
        INSTRUKSI KHUSUS (IKUTI SECARA DIAM-DIAM):
        
        1. TEKNIS: Tulis kepanjangan istilah teknis (IF, GERD, dll) saat pertama muncul.
        
        2. LOGIKA "SPIRULINA":
           SKENARIO A (BAHAYA - Ginjal/Asam Urat/Alergi Seafood):
           -> JANGAN sebut kata "Spirulina". Fokus Real Food.
           
           SKENARIO B (AMAN):
           -> Jelaskan manfaat Spirulina.
           -> Tutup penjelasan dengan kalimat: "Silakan cek rekomendasi nutrisi di bawah ini."
        
        3. OUTPUT: Langsung berikan jawaban yang ramah dan sistematis dalam bentuk poin panduan.
        
        4. ANALISA PUASA PANJANG (PROLONGED FASTING) & OMAD:
           Buat bagian khusus berjudul "Analisa Kelayakan Puasa Panjang & Berkala".
           Lakukan evaluasi ketat berdasarkan parameter user di atas (Usia, Gender, BMI, Kondisi).
           Gunakan dasar kajian ilmiah umum (misal: kajian autofagi Dr. Yoshinori Ohsumi, regenerasi sel punca Dr. Valter Longo).
           
           - JIKA TIDAK AMAN UNTUK 48-72 JAM (Kriteria: BMI < 18.5, Usia lanjut, ada riwayat Ginjal/Jantung/Diabetes tipe 1/Kondisi lemah):
             a) Kesimpulan Tegas: Jelaskan secara ilmiah mengapa puasa 48-72 jam TIDAK DIREKOMENDASIKAN untuk profil ini (misal: risiko kehilangan massa otot, beban metabolik berlebih, atau ketidakstabilan gula darah).
             b) Alternatif OMAD (One Meal A Day / 24 Jam): Evaluasi apakah OMAD masih memungkinkan. Jika memungkinkan, berikan rekomendasi INTERVAL AMAN (misalnya: maksimal 1 hingga 2 kali seminggu, jangan setiap hari). Tegaskan pentingnya kepadatan nutrisi saat berbuka puasa untuk mencegah malnutrisi.
             
           - JIKA AMAN UNTUK 48-72 JAM (Kriteria: Dewasa sehat, BMI Normal/Overweight/Obese, tidak ada penyakit kronis sensitif):
             a) Kesimpulan: Puasa 48-72 jam MEMUNGKINKAN dan direkomendasikan.
             b) Tanda Kesiapan Fisik (Readiness): Jelaskan indikator bahwa tubuh sudah siap (misalnya: tubuh sudah "Fat-Adapted", mampu puasa 24 jam / OMAD tanpa rasa lapar berlebih, pusing, atau gemetar).
             c) Pentahapan (Wajib): Jelaskan adaptasi bertahap. Mulai dari rutinitas 16:8 -> beranjak ke OMAD (24 jam) -> puasa 36 jam -> 48 jam -> baru kemudian 72 jam.
             d) Interval / Frekuensi Pelaksanaan: Beri pedoman waktu (misalnya: Puasa 48-72 jam cukup dilakukan 1 kali sebulan atau 1 kali per kuartal, sementara OMAD bisa 2-3 kali seminggu).
             e) Timing Pelaksanaan: Sarankan waktu yang tepat (saat tingkat stres rendah, akhir pekan, atau sedang libur aktivitas fisik berat).
             f) Manfaat Ilmiah: Jelaskan manfaat jam ke-48 s/d 72 (Deep Autophagy, pembersihan protein rusak, penurunan inflamasi sistemik, dan *stem cell regeneration* / peremajaan sistem imun).
             g) Peringatan Elektrolit: Wajibkan asupan air mineral dan Elektrolit murni (Natrium, Kalium, Magnesium) selama puasa untuk mencegah dehidrasi seluler.
             
        5. POLA HARIAN DALAM SEMINGGU (WEEKLY DAILY ROUTINE):
           Buat bagian berjudul "Pola Puasa Harian dalam Seminggu".
           Berikan rekomendasi jadwal jendela puasa (Fasting Window) dan jendela makan (Eating Window) untuk 7 hari (Senin-Minggu).
           
           - JIKA USER PEMULA, LANSIA, ATAU KONDISI RENTAN: 
             Berikan pola yang KONSISTEN (SAMA) setiap hari (misalnya: 16:8 setiap hari). 
             Alasan: Tubuh memerlukan stabilitas ritme sirkadian untuk beradaptasi, membentuk kebiasaan, dan mencegah stres metabolik berlebihan.
             
           - JIKA USER SEHAT, TERBIASA, ATAU TARGET PENURUNAN BB / DEEP AUTOPHAGY: 
             Berikan pola BERSELANG-SELING (Metabolic Flexibility / Metabolic Confusion). 
             Contoh: Senin & Kamis puasa OMAD (24 jam), Selasa-Rabu-Jumat puasa 16:8, Sabtu & Minggu puasa santai 12:12 atau 14:10 (sebagai hari *refeeding*).
             Alasan: Meniru pola makan evolusioner leluhur kita, mencegah laju metabolisme basal melambat (menghindari fase plateau), dan menjaga keseimbangan hormon tiroid/leptin.
             
           Format keluaran harus berupa daftar hari yang mudah dibaca (Senin sampai Minggu).
        """
        
        with st.spinner('Sedang menyusun panduan kesehatan & analisa puasa panjang Anda...'):
            response = model.generate_content(prompt_sistem)
            
            st.markdown("### 💡 Panduan & Analisa Personal")
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
                label="📄 Download PDF (Klik Disini)",
                data=file_pdf,
                file_name=f"Panduan_Sehat_{nama}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
            # PADDING BAWAH (UNTUK HALAMAN HASIL)
            st.write("\n" * 5)
            
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

