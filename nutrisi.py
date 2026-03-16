import streamlit as st
import google.generativeai as genai
import json

# --- 1. Fungsi Jaring Pengaman (Parsing) ---
def parse_nutrisi_ai(teks_respon):
    try:
        # Membersihkan teks dari kemungkinan Markdown ```json ... ```
        clean_json = teks_respon.strip().replace('```json', '').replace('```', '')
        return json.loads(clean_json)
    except Exception as e:
        st.error(f"Gagal memproses data AI: {e}")
        return None

# --- 2. Cek Akses & Data Dasar ---
if 'user_profile' not in st.session_state:
    st.warning("⚠️ Silakan isi data diri di halaman utama (app.py) terlebih dahulu.")
    st.stop()

data_dasar = st.session_state['user_profile']

st.title("🥗 Modul Nutrisi Pintar")
st.subheader(f"Halo, {data_dasar['nama']}!")

# --- 3. Input Tambahan Khusus Nutrisi ---
st.markdown("---")
st.write("Untuk saran menu yang lebih aman, silakan lengkapi data alergi Anda:")
alergi_user = st.text_input("Riwayat Alergi (kosongkan jika tidak ada):", placeholder="Contoh: Kacang, Udang, Susu Sapi...")

tombol_nutrisi = st.button("🍎 Susun Pola Nutrisi Saya", type="primary", use_container_width=True)

# --- 4. Logika AI ---
if tombol_nutrisi:
    try:
        # Konfigurasi API
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-flash-latest')

        # Menyusun JSON Prompt (Menggabungkan Data Dasar + Alergi)
        prompt_nutrisi = f"""
        TUGAS: Susun panduan nutrisi IF detil dalam format JSON.
        DATA DASAR: {data_dasar}
        RIWAYAT ALERGI BARU: {alergi_user}
        
        ATURAN:
        1. Menu wajib bebas dari alergi tersebut.
        2. Sesuaikan porsi dengan BMI ({data_dasar['bmi']:.2f}).
        3. Berikan alasan biologis untuk setiap fase makan.
        
        FORMAT OUTPUT JSON:
        {{
          "keamanan": {{"alergi_check": "teks", "catatan_medis": "teks"}},
          "menu_harian": {{
            "berbuka": {{"nama": "teks", "porsi": "teks", "alasan": "teks"}},
            "utama": {{"nama": "teks", "porsi": "teks", "alasan": "teks"}},
            "penutup": {{"nama": "teks", "porsi": "teks", "alasan": "teks"}}
          }},
          "superfood": {{"nama": "teks", "alasan_pilihan": "teks"}}
        }}
        """

        with st.spinner('AI sedang meracik nutrisi yang aman untuk Anda...'):
            response = model.generate_content(prompt_nutrisi)
            data_json = parse_nutrisi_ai(response.text)

            if data_json:
                # --- 5. Menampilkan Hasil (Parsing ke UI) ---
                st.success("✅ Analisa Nutrisi Berhasil Disusun!")
                
                # Tampilan Header Keamanan
                with st.expander("🛡️ Laporan Keamanan & Alergi", expanded=True):
                    st.write(f"**Status Alergi:** {data_json['keamanan']['alergi_check']}")
                    st.write(f"**Catatan Medis:** {data_json['keamanan']['catatan_medis']}")

                # Tampilan Menu dengan Tabs
                tab1, tab2, tab3 = st.tabs(["🌅 Berbuka", "🍽️ Makan Utama", "🌙 Persiapan Puasa"])
                
                with tab1:
                    m = data_json['menu_harian']['berbuka']
                    st.markdown(f"### {m['nama']}")
                    st.info(f"**Porsi:** {m['porsi']}")
                    st.write(f"**Alasan Biologis:** {m['alasan']}")

                with tab2:
                    m = data_json['menu_harian']['utama']
                    st.markdown(f"### {m['nama']}")
                    st.info(f"**Porsi:** {m['porsi']}")
                    st.write(f"**Alasan Biologis:** {m['alasan']}")

                with tab3:
                    m = data_json['menu_harian']['penutup']
                    st.markdown(f"### {m['nama']}")
                    st.info(f"**Porsi:** {m['porsi']}")
                    st.write(f"**Alasan Biologis:** {m['alasan']}")

                # Rekomendasi Superfood
                st.markdown("---")
                st.subheader("🌿 Rekomendasi Superfood Pendamping")
                st.success(f"**{data_json['superfood']['nama']}**")
                st.write(data_json['superfood']['alasan_pilihan'])

    except Exception as e:
        st.error(f"Terjadi kesalahan teknis: {e}")
