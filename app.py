import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import pytz

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Expert Stock Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- KEAMANAN PASSWORD (SECRETS) ---
try:
    PASSWORD_RAHASIA = st.secrets["PASSWORD_RAHASIA"]
except FileNotFoundError:
    PASSWORD_RAHASIA = "12345" # Password cadangan lokal

# Link Pembelian
LINK_LYNK_ID = "https://lynk.id/hahastoresby"

# ==========================================
# 2. CSS CUSTOM (TAMPILAN)
# ==========================================
def local_css():
    st.markdown("""
    <style>
    /* Tombol Beli Merah */
    a[href^="https://lynk.id"] {
        background-color: #ff4b4b;
        color: white;
        text-decoration: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        display: block;
        text-align: center;
        font-weight: bold;
        border: 1px solid #ff4b4b;
    }
    a[href^="https://lynk.id"]:hover {
        background-color: #cc0000;
        border-color: #cc0000;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. FUNGSI HALAMAN BERANDA
# ==========================================
def halaman_beranda():
    st.title("🏠 Dashboard Utama")
    st.markdown("---")
    col_img, col_text = st.columns([1, 2])
    with col_img:
        st.image("https://images.unsplash.com/photo-1611974765270-ca1258634369?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", use_container_width=True)
    with col_text:
        st.subheader("Selamat Datang di Expert Stock Pro!")
        st.write("""
        Gunakan menu di sebelah kiri untuk mengakses berbagai fitur analisa saham.
        Screener harian kini sudah dilengkapi dengan indikator **RSI** untuk meningkatkan akurasi.
        """)
    
    st.markdown("### 📋 Panduan Fitur")
    c1, c2 = st.columns(2)
    with c1:
        st.info("**🔍 1. Screening Saham Harian**\nMencari peluang berdasarkan Trend, Volume, MACD, dan RSI.")
    with c2:
        st.info("**📈 2. Analisa Teknikal**\nAnalisa mendalam chart dan indikator per saham.")

# ==========================================
# 4. FUNGSI FITUR SCREENING (UPGRADED WITH RSI)
# ==========================================
def fitur_screening():
    st.title("🔍 Screening Saham: Top 50 + RSI & MACD")
    st.markdown("---")

    # Sinkronisasi Waktu
    wib = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(wib)
    
    st.info(f"""
    **📅 Waktu:** {now.strftime('%d %B %Y - %H:%M')} WIB
    **🎯 Indikator Skor:** MA Trend + Vol Spike + MACD + **RSI Momentum**
    """)

    tombol_scan = st.button("Mulai Screening (Proses ±60 Detik)")

    saham_top50 = [
        "BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK", "BBTN.JK", "BRIS.JK", "ARTO.JK", "BFIN.JK",
        "BREN.JK", "TPIA.JK", "BRPT.JK", "PGEO.JK", "AMMN.JK",
        "TLKM.JK", "ISAT.JK", "EXCL.JK", "TOWR.JK", "MTEL.JK",
        "GOTO.JK", "BUKA.JK", "EMTK.JK",
        "ADRO.JK", "ANTM.JK", "MDKA.JK", "PTBA.JK", "INCO.JK", 
        "PGAS.JK", "MEDC.JK", "AKRA.JK", "HRUM.JK", "ITMG.JK", "TINS.JK", "MBMA.JK",
        "ICBP.JK", "INDF.JK", "UNVR.JK", "AMRT.JK", "CPIN.JK", "MYOR.JK", "ACES.JK", "MAPI.JK",
        "CTRA.JK", "SMRA.JK", "BSDE.JK", "PWON.JK", "PANI.JK",
        "ASII.JK", "UNTR.JK", "KLBF.JK", "JSMR.JK"
    ]

    if tombol_scan:
        hasil_lolos = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        total = len(saham_top50)

        for i, ticker in enumerate(saham_top50):
            progress_bar.progress((i + 1) / total)
            status_text.text(f"Menganalisa ({i+1}/{total}): {ticker}...")
            try:
                stock = yf.Ticker(ticker)
                df = stock.history(period="6mo") 
                if len(df) < 55: continue

                curr = df['Close'].iloc[-1]
                prev = df['Close'].iloc[-2]
                vol = df['Volume'].iloc[-1]
                
                # 1. MA Trend
                df['MA20'] = df['Close'].rolling(20).mean()
                df['MA50'] = df['Close'].rolling(50).mean()
                df['VolMA20'] = df['Volume'].rolling(20).mean()

                # 2. RSI Calculation (14)
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                df['RSI'] = 100 - (100 / (1 + rs))
                curr_rsi = df['RSI'].iloc[-1]

                # 3. MACD
                exp12 = df['Close'].ewm(span=12, adjust=False).mean()
                exp26 = df['Close'].ewm(span=26, adjust=False).mean()
                macd = exp12 - exp26
                signal = macd.ewm(span=9, adjust=False).mean()

                # Filter Dasar
                if curr > 55 and curr > df['MA20'].iloc[-1] > df['MA50'].iloc[-1] and (curr*vol) > 10_000_000_000:
                    
                    # Support/Resist
                    supp = df['Low'].tail(20).min()
                    res = df['High'].tail(20).max()
                    risk = ((supp - curr) / curr) * 100
                    reward = ((res - curr) / curr) * 100

                    # SCORING SYSTEM (Max 100)
                    score = 40 # Base score lolos filter trend
                    
                    # Bonus Volume (+15)
                    if vol > df['VolMA20'].iloc[-1]: score += 15
                    
                    # Bonus MACD (+15)
                    if macd.iloc[-1] > signal.iloc[-1]: score += 15
                    
                    # BONUS RSI (+15) - Area Golden Momentum
                    if 50 <= curr_rsi <= 68:
                        score += 15
                    elif curr_rsi > 75:
                        score -= 10 # Penalti karena sudah Overbought

                    # Bonus Risk/Reward (+15)
                    if reward > (abs(risk) * 1.5): score += 15

                    if score >= 85: label = "⭐⭐⭐⭐⭐ (Sangat Kuat)"
                    elif score >= 70: label = "⭐⭐⭐⭐ (Kuat)"
                    else: label = "⭐⭐⭐ (Cukup)"

                    hasil_lolos.append({
                        "Ticker": ticker.replace(".JK", ""),
                        "Harga": curr,
                        "Chg (%)": round(((curr-prev)/prev)*100, 2),
                        "RSI": round(curr_rsi, 1),
                        "Confidence": f"{score}%",
                        "Rating": label,
                        "Value (M)": round((curr*vol)/1e9, 1),
                        "Support": supp, "Resist": res,
                        "Risk (%)": round(risk, 2), "Reward (%)": round(reward, 2),
                        "Raw_Score": score
                    })
            except: continue 

        progress_bar.empty()
        status_text.empty()

        if hasil_lolos:
            hasil_lolos.sort(key=lambda x: x['Raw_Score'], reverse=True)
            st.success(f"Berhasil menjaring {len(hasil_lolos)} saham potensial!")
            st.dataframe(pd.DataFrame(hasil_lolos)[["Ticker", "Rating", "Harga", "RSI", "Confidence", "Value (M)"]], use_container_width=True)
            
            st.subheader("📝 Trading Plan Strategis")
            for item in hasil_lolos:
                title = f"{'🔥' if '⭐⭐⭐⭐⭐' in item['Rating'] else '✅'} {item['Ticker']} | RSI: {item['RSI']} | Skor: {item['Confidence']}"
                with st.expander(title):
                    c1, c2, c3 = st.columns(3)
                    with c1: st.metric("Entry", f"{item['Harga']:,.0f}")
                    with c2: st.metric("Stop Loss", f"{item['Support']:,.0f}", f"{item['Risk (%)']}%")
                    with c3: st.metric("Target", f"{item['Resist']:,.0f}", f"+{item['Reward (%)']}%")
                    st.write(f"**Analisa:** Saham {item['Ticker']} dalam kondisi {item['Rating']}. RSI berada di angka {item['RSI']} yang menunjukkan {'momentum kuat' if item['RSI'] > 50 else 'pemulihan trend'}.")
        else:
            st.warning("Belum ada saham yang memenuhi kriteria kombinasi Trend, Volume, MACD, dan RSI hari ini.")

# --- FITUR LAIN (PLACEHOLDER) ---
def fitur_teknikal():
    st.title("📈 Analisa Teknikal")
    st.info("Fitur ini akan kita isi di tahap selanjutnya.")

def fitur_perbandingan():
    st.title("⚖️ Perbandingan Saham")
    st.info("Fitur ini akan kita isi di tahap selanjutnya.")

def fitur_fundamental():
    st.title("📊 Analisa Fundamental")
    st.info("Fitur ini akan kita isi di tahap selanjutnya.")

def fitur_dividen():
    st.title("💰 Analisa Dividen")
    st.info("Fitur ini akan kita isi di tahap selanjutnya.")

# ==========================================
# 5. LOGIKA UTAMA
# ==========================================
if 'status_login' not in st.session_state:
    st.session_state['status_login'] = False

def main():
    local_css()
    if not st.session_state['status_login']:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h1 style='text-align: center;'>📈 Expert Stock Pro</h1>", unsafe_allow_html=True)
            st.markdown("---")
            input_pass = st.text_input("Password Premium", type="password")
            if st.button("Masuk Aplikasi", use_container_width=True):
                if input_pass == PASSWORD_RAHASIA:
                    st.session_state['status_login'] = True
                    st.rerun()
                else: st.error("Password Salah.")
            st.link_button("🛒 Beli Akses Premium", LINK_LYNK_ID, use_container_width=True)
    else:
        with st.sidebar:
            st.header("Expert Stock Pro")
            pilihan_menu = st.radio("Pilih Menu:", ("🏠 Beranda", "🔍 1. Screening Harian", "📈 2. Analisa Teknikal", "⚖️ 3. Perbandingan Saham", "📊 4. Analisa Fundamental", "💰 5. Analisa Dividen"))
            if st.button("Keluar"):
                st.session_state['status_login'] = False
                st.rerun()

        if pilihan_menu == "🏠 Beranda": halaman_beranda()
        elif pilihan_menu == "🔍 1. Screening Harian": fitur_screening()
        elif pilihan_menu == "📈 2. Analisa Teknikal": fitur_teknikal()
        elif pilihan_menu == "⚖️ 3. Perbandingan Saham": fitur_perbandingan()
        elif pilihan_menu == "📊 4. Analisa Fundamental": fitur_fundamental()
        elif pilihan_menu == "💰 5. Analisa Dividen": fitur_dividen()

if __name__ == "__main__":
    main()
