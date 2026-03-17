import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime, timedelta, timezone

# --- FUNGSI PEMBUAT PDF (KHUSUS NUTRISI) ---
def create_pdf_nutrisi(teks_analisa, nama_user, usia_user, logo_path="Logo_Aplikasi_Sehat.png"):
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
    subjudul = "Panduan Menu Nutrisi Jendela Makan & Rekomendasi Superfood yang Dirancang Khusus untuk Anda"
    pdf.multi_cell(165, 5, subjudul)
    
    pdf.set_y(35)
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(0, 0, 255)  
    pdf.cell(0, 5, "Sumber: https://aplikasisehat.streamlit.app", ln=True, align='C', link="https://aplikasisehat.streamlit.app")
    pdf.ln(2)
    
    pdf.set_text_color(0, 0, 0) 
    pdf.set_font("Arial", 'B', 16)
    aman_nama = nama_user.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 8, f"Menu & Nutrisi Klien: {aman_nama}", ln=True, align='C')
    
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
    pdf.cell(0, 5, "Konsultasi & Order Superfood (Spirulina & Black Garlic):", ln=True, align='C')
    pdf.set_text_color(0, 0, 255) 
    pdf.cell(0, 5, "WA: 0818.0202.6090", ln=True, align='C', link="https://wa.me/6281802026090")
    
    return pdf.output(dest="S").encode("latin-1")

def render_halaman(model, parse_ai_json):
    st.markdown("### 🥗 Modul Nutrisi Khusus")
    
    if 'user_profile' not in st.session_state:
        st.warning("⚠️ Silakan isi data diri Anda di menu **1️⃣ Profil Data Diri** terlebih dahulu.")
        return 

    data = st.session_state['user_profile']
    nama_klien = data['nama']
    usia_klien = data['usia']
    
    st.info(f"Profil aktif: **{nama_klien}** | Usia: **{usia_klien} th** | BMI: **{data['bmi']:.2f}**")
    
    alergi = st.text_input("Apakah Anda memiliki Alergi Makanan tertentu?", placeholder="Contoh: Kacang, Telur, Seafood. Kosongkan jika tidak ada.")
    
    if st.button("🍎 Susun Pola Nutrisi Saya", type="primary", use_container_width=True):
        
        prompt_nutrisi = f"""
        TUGAS: Susun nutrisi jendela makan dan edukasi superfood dengan format JSON murni.
        DATA UMUM: Usia {usia_klien}, Gender {data['gender']}, BMI {data['bmi']:.2f}, Kondisi: {data['kondisi']}.
        ALERGI: {alergi if alergi else 'Tidak ada'}.
        
        ATURAN JSON WAJIB:
        {{
          "keamanan": "Teks penjelasan mengapa menu ini aman untuk kondisinya dan alerginya.",
          "menu": {{
            "berbuka": {{"nama": "teks", "alasan": "teks"}},
            "utama": {{"nama": "teks", "alasan": "teks"}},
            "penutup": {{"nama": "teks", "alasan": "teks"}}
          }},
          "edukasi_spirulina": {{
            "alasan_medis_personal": "1 paragraf persuasif mengapa user spesifik ini SANGAT MEMBUTUHKAN Spirulina. Kaitkan dengan usia, anti-aging, atau nutrisi sel.",
            "dukungan_autofagi": "1 paragraf singkat bagaimana Spirulina menjaga energi/otot selama puasa IF."
          }},
          "edukasi_black_garlic": {{
            "alasan_medis_personal": "1 paragraf persuasif mengapa Black Garlic spesifik cocok untuk user ini. Kaitkan dengan kondisi medisnya (hipertensi/kolesterol/gula darah) atau imunitas.",
            "sinergi_dengan_puasa": "1 paragraf singkat bagaimana Black Garlic mengoptimalkan pembersihan pembuluh darah dan antioksidan saat puasa IF."
          }}
        }}
        """
        
        with st.spinner("Meracik menu dan menganalisa kebutuhan nutrisi seluler Anda..."):
            try:
                resp_nutrisi = model.generate_content(prompt_nutrisi)
                json_data = parse_ai_json(resp_nutrisi.text)
                
                if json_data:
                    st.success("✅ Menu Nutrisi Berhasil Disusun!")
                    st.write(f"**🛡️ Catatan Ahli:** {json_data['keamanan']}")
                    
                    st.markdown(f"**🌅 Saat Berbuka:** {json_data['menu']['berbuka']['nama']}")
                    st.caption(f"*Alasan:* {json_data['menu']['berbuka']['alasan']}")
                    
                    st.markdown(f"**🍽️ Makan Utama:** {json_data['menu']['utama']['nama']}")
                    st.caption(f"*Alasan:* {json_data['menu']['utama']['alasan']}")
                    
                    st.markdown(f"**🌙 Sebelum Puasa:** {json_data['menu']['penutup']['nama']}")
                    st.caption(f"*Alasan:* {json_data['menu']['penutup']['alasan']}")
                    
                    st.divider()
                    
                    # --- MENYIAPKAN VARIABEL UNTUK TEKS PDF ---
                    teks_untuk_pdf = f"### I. CATATAN KEAMANAN MEDIS\n{json_data['keamanan']}\n\n"
                    teks_untuk_pdf += f"### II. REKOMENDASI MENU HARIAN\n"
                    teks_untuk_pdf += f"- Saat Berbuka: {json_data['menu']['berbuka']['nama']}\n  Alasan Medis: {json_data['menu']['berbuka']['alasan']}\n\n"
                    teks_untuk_pdf += f"- Makan Utama: {json_data['menu']['utama']['nama']}\n  Alasan Medis: {json_data['menu']['utama']['alasan']}\n\n"
                    teks_untuk_pdf += f"- Sebelum Puasa (Penutup): {json_data['menu']['penutup']['nama']}\n  Alasan Medis: {json_data['menu']['penutup']['alasan']}\n\n"
                    teks_untuk_pdf += f"### III. EDUKASI SUPERFOOD KHUSUS UNTUK ANDA\n"
                    
                    # --- LOGIKA PENAMPILAN SUPERFOOD ---
                    kata_bahaya_spirulina = ["ginjal", "gagal", "cuci darah", "ckd", "hemo", "kreatinin", "asam urat", "alergi seafood"]
                    is_spirulina_aman = not any(k in data['kondisi'].lower() for k in kata_bahaya_spirulina)
                    
                    pesan_wa_produk = "Black%20Garlic" # Default jika spirulina tidak aman
                    
                    st.subheader("🌿 Rekomendasi Superfood Pendamping")
                    
                    # 1. Tampilkan Black Garlic (Selalu aman dan direkomendasikan)
                    with st.expander("🧄 Black Garlic (Bawang Hitam Fermentasi)", expanded=True):
                        st.markdown(f"*{json_data['edukasi_black_garlic']['alasan_medis_personal']}*")
                        st.markdown(f"**Sinergi Puasa:** {json_data['edukasi_black_garlic']['sinergi_dengan_puasa']}")
                        
                        teks_untuk_pdf += f"**A. Black Garlic (Bawang Hitam Fermentasi)**\n"
                        teks_untuk_pdf += f"{json_data['edukasi_black_garlic']['alasan_medis_personal']}\n"
                        teks_untuk_pdf += f"Sinergi Puasa: {json_data['edukasi_black_garlic']['sinergi_dengan_puasa']}\n\n"

                    # 2. Tampilkan Spirulina (Hanya jika lolos filter keamanan)
                    if is_spirulina_aman:
                        pesan_wa_produk = "Spirulina%20dan%20Black%20Garlic"
                        with st.expander("🌱 Spirulina Grade A (Mikroalga Hijau-Biru)", expanded=True):
                            st.markdown(f"*{json_data['edukasi_spirulina']['alasan_medis_personal']}*")
                            st.markdown(f"**Optimalisasi Puasa:** {json_data['edukasi_spirulina']['dukungan_autofagi']}")
                            
                            teks_untuk_pdf += f"**B. Spirulina Grade A**\n"
                            teks_untuk_pdf += f"{json_data['edukasi_spirulina']['alasan_medis_personal']}\n"
                            teks_untuk_pdf += f"Dukungan Autofagi: {json_data['edukasi_spirulina']['dukungan_autofagi']}\n\n"
                    else:
                        st.info("Catatan: Spirulina tidak ditambahkan ke rekomendasi Anda berdasarkan filter keamanan riwayat medis (Ginjal/Asam Urat/Alergi Seafood).")

                    # --- TOMBOL ORDER WHATSAPP (GABUNGAN) ---
                    st.markdown("---")
                    st.write("Tingkatkan kualitas kesehatan sel tubuh Anda. Dapatkan produk *Superfood* murni dan terkurasi link WA 0818.0202.6090 di bawah ini:")
                    link_sp = f"https://wa.me/6281802026090?text=Halo%20kak%20Elisa,%20saya%20tertarik%20pesan%20{pesan_wa_produk}%20Rekomendasi%20Aplikasi%20Sehat."
                    st.link_button("🛒 Pesan Superfood Sekarang", link_sp, use_container_width=True)
                    
                    # --- TOMBOL DOWNLOAD PDF NUTRISI ---
                    st.divider()
                    st.write("📥 **Simpan Resep & Panduan Nutrisi Ini:**")
                    
                    file_pdf_nutrisi = create_pdf_nutrisi(teks_untuk_pdf, nama_klien, usia_klien)
                    
                    st.download_button(
                        label="📄 Download Laporan Nutrisi (PDF)",
                        data=file_pdf_nutrisi,
                        file_name=f"Menu_Nutrisi_{nama_klien}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                else:
                    st.error("Gagal membaca format dari AI. Silakan klik tombol susun kembali.")
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")
