import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime, timedelta, timezone

# --- FUNGSI PEMBUAT PDF ---
def create_pdf(teks_analisa, nama_user, usia_user, logo_path="Logo_Aplikasi_Sehat.png"):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_fill_color(20, 20, 20)  
    pdf.rect(0, 0, 210, 32, 'F')    
    
    if not os.path.exists(logo_path):
        if os.path.exists("../Logo_Aplikasi_Sehat.png"):
            logo_path = "../Logo_Aplikasi_Sehat.png"

    if os.path.exists(logo_path):
        pdf.set_fill_color(218, 165, 32)
        pdf.set_draw_color(218, 165, 32)
        pdf.ellipse(9, 5, 22, 22, 'F')
        pdf.set_fill_color(255, 255, 255) 
        pdf.ellipse(9.5, 5.5, 21, 21, 'F')
        pdf.image(logo_path, x=10.5, y=6.5, w=19, h=19)
    
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_xy(35, 6) 
    pdf.cell(0, 8, "Konsultan Hidup Sehat", ln=True)

    pdf.set_font("Arial", '', 9)
    pdf.set_text_color(220, 220, 220)
    pdf.set_xy(35, 14)
    subjudul = "Panduan Puasa Intermiten (Intermittent Fasting) sesuai Usia, Jenis Kelamin, Komposisi Tubuh, dan Riwayat Kesehatan agar Mendapatkan Autofagi yang Efektif"
    pdf.multi_cell(165, 5, subjudul)
    
    pdf.set_y(35)
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(0, 0, 255)  
    pdf.cell(0, 5, "Sumber: https://aplikasisehat.streamlit.app", ln=True, align='C', link="https://aplikasisehat.streamlit.app")
    pdf.ln(2)
    
    pdf.set_text_color(0, 0, 0) 
    pdf.set_font("Arial", 'B', 16)
    aman_nama = nama_user.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 8, f"Klien: {aman_nama} | Usia: {usia_user} Th", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 10)
    tz_wib = timezone(timedelta(hours=7)) 
    waktu_analisa = datetime.now(tz_wib).strftime("%d-%m-%Y %H:%M WIB")
    pdf.cell(0, 5, f"Waktu Cetak: {waktu_analisa}", ln=True, align='R')
    
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y()+2, 200, pdf.get_y()+2)
    pdf.ln(5)
    
    teks_bersih = teks_analisa.encode('latin-1', 'ignore').decode('latin-1')
    
    for baris in teks_bersih.split('\n'):
        baris_pdf = baris.replace('**', '').replace('### ', '').replace('## ', '').strip()
        if baris_pdf.startswith(('I.', 'II.', 'III.', 'IV.', 'V.', 'VI.', 'VII.')):
            pdf.ln(6)
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(0, 102, 204) 
            pdf.multi_cell(0, 7, baris_pdf)
            pdf.ln(1)
            pdf.set_text_color(0, 0, 0) 
        elif baris_pdf.startswith('-') or baris_pdf.startswith('*'):
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, "  " + baris_pdf)
        else:
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, baris_pdf)
            
    pdf.ln(15)
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, "Dapatkan panduan lengkap di Ebook 'Puasa Pintar'", ln=True, align='C')
    pdf.set_text_color(0, 0, 255) 
    pdf.cell(0, 5, "https://lynk.id/hahastoresby", ln=True, align='C', link="https://lynk.id/hahastoresby")
    
    return pdf.output(dest="S").encode("latin-1")

# --- FUNGSI UTAMA HALAMAN PUASA ---
def render_halaman(model):
    st.markdown("### ⏳ Panduan Puasa (IF) & Autofagi")
    
    # CEK APAKAH DATA PROFIL SUDAH DIISI
    if 'user_profile' not in st.session_state:
        st.warning("⚠️ Data Profil belum lengkap. Silakan kembali ke menu **1️⃣ Profil Data Diri** dan klik tombol 'Simpan Data Profil'.")
        return

    data = st.session_state['user_profile']
    bmi = data['bmi']
    nama = data['nama']
    usia = data['usia']

    st.info(f"Menganalisa profil: **{nama}** | Usia: **{usia} th** | BMI: **{bmi:.2f}**")
    
    if bmi < 18.5: st.warning(f"⚠️ BMI: {bmi:.2f} (Underweight)")
    elif 18.5 <= bmi < 25: st.success(f"✅ BMI: {bmi:.2f} (Normal)")
    elif 25 <= bmi < 30: st.warning(f"⚠️ BMI: {bmi:.2f} (Overweight)")
    else: st.error(f"🚨 BMI: {bmi:.2f} (Obesity)")

    if st.button("🩺 Analisa & Susun Jadwal Puasa Sehat", type="primary", use_container_width=True):
        try:
            teks_berhenti = f" (Telah berhenti {data['lama_berhenti']} bulan)" if data['lama_berhenti'] else ""
            
            prompt_sistem = f"""
            PERAN: Ahli Krononutrisi & Praktisi Kesehatan Holistik.
            DATA USER: Nama: {data['nama']}, Usia: {data['usia']}, Gender: {data['gender']}, BMI: {data['bmi']:.2f}, Pengalaman: {data['pengalaman_puasa']}{teks_berhenti}, Butuh Pemula: {data['butuh_panduan_pemula']}, Kondisi: {data['kondisi']}, Tanya: {data['pertanyaan']}.
            
            FORMAT (Tanpa Judul Besar, Gunakan Markdown ### untuk Angka Romawi):
            Salam sehat {data['nama']}, ... (kalimat pembuka).
            
            ### I. ANALISA KONDISI SAAT INI
            (Isi evaluasi singkat)
            """

            if data['butuh_panduan_pemula'] == "Iya":
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

            with st.spinner('Sedang menyusun jadwal puasa dan analisa Autofagi Anda...'):
                response = model.generate_content(prompt_sistem)
                
                st.markdown("### 💡 Laporan Pola Puasa")
                st.markdown(response.text)
                
                st.divider()
                st.success("☝️ **Langkah Selanjutnya:** Silakan ganti pilihan menu di atas ke **3️⃣ Modul Nutrisi & Superfood** untuk melihat rekomendasi makanan Anda.")
                
                # --- BAGIAN EBOOK ---
                st.info("📘 **PANDUAN LENGKAP TERSEDIA**")
                col_promo, col_btn = st.columns([2, 1])
                with col_promo:
                    st.write("Pahami sains **Autofagi & Penyembuhan Sel**. Baca Ebook **'Puasa Pintar'**.")
                with col_btn:
                    st.link_button("📖 Order Ebook (https://lynk.id/hahastoresby", "http://lynk.id/hahastoresby/zq3l63qj96m8", use_container_width=True)

                st.divider()

                # --- DOWNLOAD PDF ---
                st.write("📥 **Simpan Panduan Ini:**")
                file_pdf = create_pdf(response.text, nama, usia)
                
                st.download_button(
                    label="📄 Download Laporan PDF (Klik Disini)",
                    data=file_pdf,
                    file_name=f"Panduan_Puasa_{nama}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
        except Exception as e:
                pesan_error = str(e).lower()
                if "429" in pesan_error or "quota" in pesan_error:
                    st.warning("⏳ Server Konsultan AI sedang sibuk melayani antrean. Silakan tunggu sekitar 1 menit, lalu klik tombol susun kembali.")
                else:
                    st.error(f"Terjadi kesalahan teknis: {e}")
