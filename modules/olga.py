import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime, timedelta, timezone

# --- FUNGSI PEMBUAT PDF (KHUSUS OLAHRAGA) ---
def create_pdf_olga(teks_analisa, nama_user, usia_user, logo_path="Logo_Aplikasi_Sehat.png"):
    pdf = FPDF()
    pdf.add_page()
    
    # Header Hitam Elegan
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
    
    # Judul & Subjudul
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_xy(35, 6) 
    pdf.cell(0, 8, "Konsultan Hidup Sehat", ln=True)

    pdf.set_font("Arial", '', 9)
    pdf.set_text_color(220, 220, 220)
    pdf.set_xy(35, 14)
    subjudul = "Panduan Olahraga, Target Detak Jantung, dan Keamanan Fisik Khusus Metode Intermittent Fasting (IF)"
    pdf.multi_cell(165, 5, subjudul)
    
    pdf.set_y(35)
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(0, 0, 255)  
    pdf.cell(0, 5, "Sumber: https://aplikasisehat.streamlit.app", ln=True, align='C', link="https://aplikasisehat.streamlit.app")
    pdf.ln(2)
    
    # Nama Klien & Tanggal
    pdf.set_text_color(0, 0, 0) 
    pdf.set_font("Arial", 'B', 16)
    aman_nama = nama_user.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 8, f"Program Latihan: {aman_nama}", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 10)
    tz_wib = timezone(timedelta(hours=7)) 
    waktu_analisa = datetime.now(tz_wib).strftime("%d-%m-%Y %H:%M WIB")
    pdf.cell(0, 5, f"Waktu Cetak: {waktu_analisa}", ln=True, align='R')
    
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y()+2, 200, pdf.get_y()+2)
    pdf.ln(5)
    
    # Cetak Isi Konten
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
            
    # Footer Ebook
    pdf.ln(15)
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, "Pelajari sains pemulihan tubuh di Ebook 'Puasa Pintar':", ln=True, align='C')
    pdf.set_text_color(0, 0, 255) 
    pdf.cell(0, 5, "https://lynk.id/hahastoresby", ln=True, align='C', link="https://lynk.id/hahastoresby")
    
    return pdf.output(dest="S").encode("latin-1")

def render_halaman(model, parse_ai_json):
    st.markdown("### 🏃 Modul Olahraga Pintar")
    
    if 'user_profile' not in st.session_state:
        st.warning("⚠️ Data Profil belum lengkap. Silakan kembali ke menu **1️⃣ Profil Data Diri** dan klik 'Simpan Data Profil' terlebih dahulu.")
        return

    data = st.session_state['user_profile']
    nama_klien = data['nama']
    usia_klien = data['usia']
    
    st.info(f"Profil aktif: **{nama_klien}** | Usia: **{usia_klien} th** | BMI: **{data['bmi']:.2f}**")
    
    with st.expander("Catatan Kesehatan Anda (Klik untuk lihat)"):
        st.write(f"*{data['kondisi']}*")
    
    st.markdown("---")
    st.write("Olahraga yang tepat saat berpuasa akan mengoptimalkan pembakaran lemak (*fat oxidation*) dan memicu hormon pertumbuhan (*HGH*) untuk melindungi massa otot Anda, namun tetap harus disesuaikan dengan kapasitas tubuh.")

    if st.button("💪 Susun Jadwal Olahraga Saya", type="primary", use_container_width=True):
        
        prompt_olga = f"""
        TUGAS: Anda adalah Ahli Kebugaran Fisik (Personal Trainer) khusus metode Intermittent Fasting.
        Susun jadwal dan rekomendasi olahraga yang dipersonalisasi.
        
        DATA PENGGUNA:
        - Usia: {usia_klien} tahun
        - Gender: {data['gender']}
        - BMI: {data['bmi']:.2f}
        - Kondisi Kesehatan: {data['kondisi']}
        
        ATURAN KEAMANAN (CRITICAL):
        1. Jika BMI > 25 (Overweight/Obese) atau ada keluhan sendi/lutut pada data Kondisi Kesehatan, DILARANG menyarankan olahraga High-Impact (seperti lari, lompat, burpees). Wajib sarankan Low-Impact (renang, sepeda, jalan cepat).
        2. Jika ada riwayat hipertensi atau masalah jantung, batasi intensitas.
        3. Hitung estimasi Target Detak Jantung Maksimal (MHR = 220 - usia). Zona aman adalah 50-70% dari MHR.
        
        FORMAT OUTPUT WAJIB JSON MURNI:
        {{
          "peringatan_medis": "Peringatan keamanan khusus berdasarkan kondisi medis dan BMI klien.",
          "latihan_jendela_puasa": {{
            "jenis": "Saran kardio intensitas rendah (LISS)",
            "durasi_menit": "Contoh: 30-45",
            "alasan": "Penjelasan mengapa ini membakar lemak secara efektif"
          }},
          "latihan_jendela_makan": {{
            "jenis": "Saran latihan kekuatan/beban",
            "durasi_menit": "Contoh: 20-30",
            "alasan": "Penjelasan terkait pembentukan otot dengan glikogen terisi"
          }},
          "target_detak_jantung": {{
            "zona_aman": "Rentang BPM (Beat Per Minute) hasil hitungan MHR",
            "penjelasan": "Cara mudah mengukur intensitas tanpa alat (misal: 'Talk Test' atau 'masih bisa ngobrol santai')"
          }}
        }}
        """
        
        with st.spinner("Mendesain program latihan dan menghitung batas detak jantung Anda..."):
            try:
                resp_olga = model.generate_content(prompt_olga)
                json_olga = parse_ai_json(resp_olga.text)
                
                if json_olga:
                    st.success("✅ Jadwal Olahraga Berhasil Disusun!")
                    
                    # --- MENAMPILKAN KE LAYAR HP ---
                    st.error(f"**⚠️ PERINGATAN KEAMANAN:**\n{json_olga['peringatan_medis']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info("🕒 **Saat Jendela Puasa** *(Fasted State)*")
                        st.write(f"**Jenis Latihan:** {json_olga['latihan_jendela_puasa']['jenis']}")
                        st.write(f"**Durasi:** `{json_olga['latihan_jendela_puasa']['durasi_menit']} Menit`")
                        st.caption(f"💡 *Tujuan:* {json_olga['latihan_jendela_puasa']['alasan']}")
                        
                    with col2:
                        st.success("🍽️ **Saat Jendela Makan** *(Fed State)*")
                        st.write(f"**Jenis Latihan:** {json_olga['latihan_jendela_makan']['jenis']}")
                        st.write(f"**Durasi:** `{json_olga['latihan_jendela_makan']['durasi_menit']} Menit`")
                        st.caption(f"💡 *Tujuan:* {json_olga['latihan_jendela_makan']['alasan']}")
                        
                    st.markdown("---")
                    st.markdown("### 💓 Target Detak Jantung (*Heart Rate*)")
                    st.markdown(f"**Zona Aman Anda:** `{json_olga['target_detak_jantung']['zona_aman']}`")
                    st.write(f"**Indikator Praktis:** {json_olga['target_detak_jantung']['penjelasan']}")
                    
                    # --- MERANGKAI TEKS UNTUK DICETAK KE PDF ---
                    teks_untuk_pdf = f"### I. PERINGATAN KEAMANAN MEDIS\n{json_olga['peringatan_medis']}\n\n"
                    
                    teks_untuk_pdf += f"### II. JADWAL LATIHAN HARIAN\n"
                    teks_untuk_pdf += f"- SAAT JENDELA PUASA (Fasted State):\n"
                    teks_untuk_pdf += f"  * Jenis Latihan: {json_olga['latihan_jendela_puasa']['jenis']}\n"
                    teks_untuk_pdf += f"  * Durasi: {json_olga['latihan_jendela_puasa']['durasi_menit']} Menit\n"
                    teks_untuk_pdf += f"  * Tujuan: {json_olga['latihan_jendela_puasa']['alasan']}\n\n"
                    
                    teks_untuk_pdf += f"- SAAT JENDELA MAKAN (Fed State):\n"
                    teks_untuk_pdf += f"  * Jenis Latihan: {json_olga['latihan_jendela_makan']['jenis']}\n"
                    teks_untuk_pdf += f"  * Durasi: {json_olga['latihan_jendela_makan']['durasi_menit']} Menit\n"
                    teks_untuk_pdf += f"  * Tujuan: {json_olga['latihan_jendela_makan']['alasan']}\n\n"
                    
                    teks_untuk_pdf += f"### III. TARGET DETAK JANTUNG & INTENSITAS\n"
                    teks_untuk_pdf += f"Zona Aman Anda: {json_olga['target_detak_jantung']['zona_aman']}\n"
                    teks_untuk_pdf += f"Indikator Praktis: {json_olga['target_detak_jantung']['penjelasan']}\n"

                    # --- TOMBOL DOWNLOAD PDF OLAHRAGA ---
                    st.divider()
                    st.write("📥 **Simpan Panduan Olahraga Ini:**")
                    
                    file_pdf_olga = create_pdf_olga(teks_untuk_pdf, nama_klien, usia_klien)
                    
                    st.download_button(
                        label="📄 Download Laporan Olahraga (PDF)",
                        data=file_pdf_olga,
                        file_name=f"Panduan_Olahraga_{nama_klien}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                else:
                    st.error("Gagal membaca format data dari AI. Silakan coba klik tombol susun kembali.")
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")
