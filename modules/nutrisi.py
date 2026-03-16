import streamlit as st

def render_halaman(model, parse_ai_json):
    st.markdown("### 🥗 Modul Nutrisi Khusus")
    
    if 'user_profile' not in st.session_state:
        st.warning("⚠️ Silakan isi data diri Anda di menu **1️⃣ Profil Data Diri** terlebih dahulu.")
        return # Menghentikan fungsi jika data kosong

    data = st.session_state['user_profile']
    st.info(f"Profil aktif: **{data['nama']}** | Usia: **{data['usia']} th** | BMI: **{data['bmi']:.2f}**")
    
    alergi = st.text_input("Apakah Anda memiliki Alergi Makanan tertentu?", placeholder="Contoh: Kacang, Telur, Seafood. Kosongkan jika tidak ada.")
    
    if st.button("🍎 Susun Pola Nutrisi Saya", type="primary", use_container_width=True):
        
        # --- UPDATE JSON PROMPT DI SINI ---
        prompt_nutrisi = f"""
        TUGAS: Susun nutrisi jendela makan dan edukasi superfood dengan format JSON murni.
        DATA UMUM: Usia {data['usia']}, Gender {data['gender']}, BMI {data['bmi']:.2f}, Kondisi: {data['kondisi']}.
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
            "alasan_medis_personal": "Buat 1 paragraf persuasif dan ilmiah mengapa pengguna spesifik ini (ingat Usia, Gender, BMI, dan Kondisi kesehatannya) SANGAT MEMBUTUHKAN Spirulina. Kaitkan dengan anti-aging, nutrisi sel, atau metabolisme.",
            "dukungan_autofagi": "Buat 1 paragraf singkat bagaimana Spirulina menjaga energi dan otot pengguna selama menjalankan puasa IF agar Autofagi maksimal."
          }}
        }}
        """
        
        with st.spinner("Meracik menu dan menganalisa kebutuhan nutrisi seluler Anda..."):
            resp_nutrisi = model.generate_content(prompt_nutrisi)
            json_data = parse_ai_json(resp_nutrisi.text)
            
            if json_data:
                st.success("✅ Menu Nutrisi Berhasil Disusun!")
                st.write(f"**🛡️ Catatan Ahli:** {json_data['keamanan']}")
                
                # Menampilkan Menu
                st.markdown(f"**🌅 Saat Berbuka:** {json_data['menu']['berbuka']['nama']}")
                st.caption(f"*Alasan:* {json_data['menu']['berbuka']['alasan']}")
                
                st.markdown(f"**🍽️ Makan Utama:** {json_data['menu']['utama']['nama']}")
                st.caption(f"*Alasan:* {json_data['menu']['utama']['alasan']}")
                
                st.markdown(f"**🌙 Sebelum Puasa:** {json_data['menu']['penutup']['nama']}")
                st.caption(f"*Alasan:* {json_data['menu']['penutup']['alasan']}")
                
                st.divider()
                
                # --- LOGIKA SPIRULINA YANG DIPERBARUI ---
                kata_bahaya = ["ginjal", "gagal", "cuci darah", "ckd", "hemo", "kreatinin", "asam urat", "alergi seafood"]
                is_spirulina_aman = not any(k in data['kondisi'].lower() for k in kata_bahaya)
                
                if is_spirulina_aman:
                    st.info("🌿 **SUPERFOOD PENDAMPING: SPIRULINA GRADE A**")
                    
                    # Menampilkan hasil copywriting AI yang sudah dipersonalisasi
                    st.markdown(f"*{json_data['edukasi_spirulina']['alasan_medis_personal']}*")
                    st.markdown(f"**Optimalisasi Puasa:** {json_data['edukasi_spirulina']['dukungan_autofagi']}")
                    
                    st.markdown("---")
                    st.write("Dapatkan Spirulina murni standar *Food Grade* (bukan untuk masker/pakan) melalui tautan di bawah ini:")
                    link_sp = "https://wa.me/6281801016090?text=Halo%20kak%20Elisa,%20saya%20tertarik%20pesan%20Spirulina%20Rekomendasi%20Aplikasi%20Sehat."
                    st.link_button("🛒 Pesan Spirulina Sekarang", link_sp, use_container_width=True)
            else:
                st.error("Gagal menyusun menu. Silakan klik tombol susun kembali.")
