import streamlit as st

def render_halaman(model, parse_ai_json):
    st.markdown("### 🏃 Modul Olahraga Pintar")
    
    # --- 1. CEK DATA PROFIL ---
    if 'user_profile' not in st.session_state:
        st.warning("⚠️ Data Profil belum lengkap. Silakan kembali ke menu **1️⃣ Profil Data Diri** dan klik 'Simpan Data Profil' terlebih dahulu.")
        return

    data = st.session_state['user_profile']
    
    # --- 2. HEADER INFO KLIEN ---
    st.info(f"Profil aktif: **{data['nama']}** | Usia: **{data['usia']} th** | BMI: **{data['bmi']:.2f}**")
    
    # Menampilkan ulang ringkasan kondisi medis agar user ingat
    with st.expander("Catatan Kesehatan Anda (Klik untuk lihat)"):
        st.write(f"*{data['kondisi']}*")
    
    st.markdown("---")
    st.write("Olahraga yang tepat saat berpuasa akan mengoptimalkan pembakaran lemak (*fat oxidation*) dan memicu hormon pertumbuhan (*HGH*) untuk melindungi massa otot Anda, namun tetap harus disesuaikan dengan kapasitas tubuh.")

    # --- 3. TOMBOL EKSEKUSI ---
    if st.button("💪 Susun Jadwal Olahraga Saya", type="primary", use_container_width=True):
        
        # --- 4. JSON PROMPT LOGIC ---
        prompt_olga = f"""
        TUGAS: Anda adalah Ahli Kebugaran Fisik (Personal Trainer) khusus metode Intermittent Fasting.
        Susun jadwal dan rekomendasi olahraga yang dipersonalisasi.
        
        DATA PENGGUNA:
        - Usia: {data['usia']} tahun
        - Gender: {data['gender']}
        - BMI: {data['bmi']:.2f}
        - Kondisi Kesehatan: {data['kondisi']}
        
        ATURAN KEAMANAN (CRITICAL):
        1. Jika BMI > 25 (Overweight/Obese) atau ada keluhan sendi/lutut pada data Kondisi Kesehatan, DILARANG menyarankan olahraga High-Impact (seperti lari, lompat, burpees). Wajib sarankan Low-Impact (renang, sepeda, jalan cepat).
        2. Jika ada riwayat hipertensi atau masalah jantung, batasi intensitas.
        3. Hitung estimasi Target Detak Jantung Maksimal (MHR = 220 - usia). Zona aman adalah 50-70% dari MHR.
        
        FORMAT OUTPUT WAJIB JSON MURNI (tanpa markdown blok kode):
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
                # Memanggil Gemini AI
                resp_olga = model.generate_content(prompt_olga)
                # Melakukan Parsing dari Teks ke JSON Object
                json_olga = parse_ai_json(resp_olga.text)
                
                if json_olga:
                    st.success("✅ Jadwal Olahraga Berhasil Disusun!")
                    
                    # --- 5. RENDER UI DARI DATA JSON ---
                    
                    # Kotak Merah/Kuning untuk Keamanan
                    st.error(f"**⚠️ PERINGATAN KEAMANAN:**\n{json_olga['peringatan_medis']}")
                    
                    # Membagi layar jadi 2 kolom untuk Fase Latihan
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
                        
                    # Bagian Detak Jantung di bawah
                    st.markdown("---")
                    st.markdown("### 💓 Target Detak Jantung (*Heart Rate*)")
                    st.markdown(f"**Zona Aman Anda:** `{json_olga['target_detak_jantung']['zona_aman']}`")
                    st.write(f"**Indikator Praktis:** {json_olga['target_detak_jantung']['penjelasan']}")
                    
                else:
                    st.error("Gagal membaca format data dari AI. Silakan coba klik tombol susun kembali.")
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")
