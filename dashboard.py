import streamlit as st
import pandas as pd
from scraper import scrape_indeed
from parser import parse_jobs
from exporter import export_to_csv

st.set_page_config(
    page_title="MyIdealJob",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif !important; }

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    visibility: hidden !important;
    display: none !important;
}

.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
.stApp { background: #ffffff !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }

/* ═══════════════════════════════════════════════════
   NAVBAR — frosted glass, léger
   ═══════════════════════════════════════════════════ */
.navbar {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 0 3rem;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    border-bottom: 1px solid rgba(14,165,233,0.08);
}
.nav-logo {
    font-size: 1.2rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.3px;
}
.nav-logo span { color: #0ea5e9; }
.nav-pill {
    background: rgba(245,158,11,0.12);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.72rem;
    font-weight: 700;
    color: #b45309;
    display: flex; align-items: center; gap: 0.4rem;
}
.live-dot {
    width: 6px; height: 6px; background: #f59e0b;
    border-radius: 50%; animation: pulse 2s infinite;
    box-shadow: 0 0 0 0 rgba(245,158,11,0.5);
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); box-shadow: 0 0 0 0 rgba(245,158,11,0.6); }
    50%      { opacity:0.7; transform:scale(1.2); box-shadow: 0 0 0 6px rgba(245,158,11,0); }
}

/* ═══════════════════════════════════════════════════
   HERO — gradient bleu plus profond, plus grand
   ═══════════════════════════════════════════════════ */
.hero-wrap {
    position: relative;
    background: linear-gradient(-45deg, #0369a1, #0284c7, #0ea5e9, #0369a1);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    padding: 5.5rem 3rem 4.5rem;
    overflow: hidden;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
/* Overlay subtil sur le hero pour texture */
.hero-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle at 20% 30%, rgba(255,255,255,0.12) 0%, transparent 45%),
                      radial-gradient(circle at 80% 70%, rgba(255,255,255,0.08) 0%, transparent 45%);
    pointer-events: none;
}
.hero-inner { position: relative; z-index: 2; }

.hero-h1 {
    font-size: 5.8rem;
    font-weight: 800;
    letter-spacing: -3.5px;
    line-height: 0.98;
    color: white;
    margin: 0 0 1.2rem;
    text-shadow: 0 4px 30px rgba(0,0,0,0.15);
}
.hero-h1 em {
    font-style: normal;
    color: #ffffff;
    position: relative;
    display: inline-block;
}
.hero-h1 em::after {
    content: '';
    position: absolute;
    bottom: 6px;
    left: 0;
    right: 0;
    height: 14px;
    background: rgba(255,255,255,0.22);
    z-index: -1;
    border-radius: 4px;
}
.hero-sub {
    font-size: 1.05rem;
    color: rgba(255,255,255,0.9);
    line-height: 1.6;
    margin: 0;
    font-weight: 500;
}

/* ═══════════════════════════════════════════════════
   FORM — blanc, bordure bleu ciel
   ═══════════════════════════════════════════════════ */
[data-testid="stForm"] {
    background: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 20px rgba(14,165,233,0.08) !important;
    padding: 2rem 3rem 2.5rem !important;
    margin: 0 !important;
    border-bottom: 1px solid #e0f2fe !important;
}

/* Labels du form — bleu vif */
[data-testid="stForm"] [data-testid="stWidgetLabel"] {
    display: block !important;
    font-size: 0.78rem !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.8px !important;
    color: #0ea5e9 !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stForm"] [data-testid="stWidgetLabel"] p {
    font-size: 0.78rem !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.8px !important;
    color: #0ea5e9 !important;
    margin: 0 !important;
}

/* Hide "Press Enter to submit form" instruction */
[data-testid="InputInstructions"],
[data-testid="stFormSubmitButton"] ~ [data-testid="InputInstructions"],
div[class*="InputInstructions"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    width: 0 !important;
    opacity: 0 !important;
    position: absolute !important;
    pointer-events: none !important;
}

/* Text inputs — blanc avec bordure bleu clair */
[data-testid="stForm"] input[type="text"] {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
    font-size: 0.9rem !important;
    caret-color: #0ea5e9 !important;
}
[data-testid="stForm"] input[type="text"]::placeholder {
    color: #94a3b8 !important;
}
[data-testid="stForm"] div[data-baseweb="input"] {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    transition: all 0.2s !important;
}
[data-testid="stForm"] div[data-baseweb="input"]:focus-within {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 3px rgba(14,165,233,0.15) !important;
    background: #ffffff !important;
}

/* ═══════════════════════════════════════════════════
   SLIDER — bleu ciel
   ═══════════════════════════════════════════════════ */
div[data-testid="stSlider"] .e2ups023,
[data-testid="stForm"] div[data-testid="stSlider"] .e2ups023 {
    background: #0ea5e9 !important;
    border-radius: 4px !important;
}
div[data-testid="stSlider"] .e2ups024,
[data-testid="stForm"] div[data-testid="stSlider"] .e2ups024 {
    background: #0ea5e9 !important;
}

/* Thumb invisible */
div[data-testid="stSlider"] .e2ups021,
[data-testid="stForm"] div[data-testid="stSlider"] .e2ups021 {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    width: 0 !important;
    height: 0 !important;
}

/* Thumb label = curseur visuel */
div[data-testid="stSlider"] [data-testid="stSliderThumbValue"],
[data-testid="stForm"] div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
    bottom: -0.05rem !important;
    position: absolute !important;
    transform: translateX(-50%) !important;
    white-space: nowrap !important;
    opacity: 1 !important;
    visibility: visible !important;
    z-index: 10 !important;
    background: transparent !important;
}
div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] [data-testid="stMarkdownContainer"],
[data-testid="stForm"] div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] [data-testid="stMarkdownContainer"] {
    background: #0ea5e9 !important;
    border-radius: 50px !important;
    padding: 0.18rem 0.55rem !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: fit-content !important;
    min-width: 28px !important;
    box-shadow: 0 0 0 3px rgba(14,165,233,0.25), 0 2px 8px rgba(14,165,233,0.35) !important;
    cursor: grab !important;
}
div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] p,
[data-testid="stForm"] div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] p {
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 0.7rem !important;
    margin: 0 !important;
    line-height: 1 !important;
    background: transparent !important;
}

/* Tickbar */
div[data-testid="stSlider"] [data-testid="stSliderTickBar"],
div[data-testid="stSlider"] [data-testid="stSliderTickBar"] * {
    background: transparent !important;
    background-color: transparent !important;
    opacity: 1 !important;
    visibility: visible !important;
    box-shadow: none !important;
}
div[data-testid="stSlider"] [data-testid="stSliderTickBar"] p {
    color: #0ea5e9 !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
}

/* Force tout point noir / tick mark sombre sur le rail à devenir bleu ou invisible */
div[data-testid="stSlider"] [role="slider"] ~ div,
div[data-testid="stSlider"] div[style*="background"] {
    background-color: #0ea5e9 !important;
}
/* Le petit dot noir au début du rail (tick de min) */
div[data-testid="stSlider"] [data-testid="stTickBarMin"],
div[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    background: transparent !important;
    color: #0ea5e9 !important;
}
/* Nettoyage complet des éléments décoratifs du rail */
div[data-testid="stSlider"] > div > div > div > div {
    background-color: #0ea5e9 !important;
}

/* ═══════════════════════════════════════════════════
   BUTTON Rechercher — bleu vif plein
   ═══════════════════════════════════════════════════ */
[data-testid="stForm"] button,
.stButton > button {
    background: #0ea5e9 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
    padding: 0.7rem 1.4rem !important;
    width: 100% !important;
    white-space: nowrap !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 12px rgba(14,165,233,0.35) !important;
}
[data-testid="stForm"] button:hover,
.stButton > button:hover {
    background: #0284c7 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(14,165,233,0.45) !important;
}

/* ═══════════════════════════════════════════════════
   STATS STRIP — fond blanc, counter animé
   ═══════════════════════════════════════════════════ */
.stats-strip {
    background: linear-gradient(to right, #f0f9ff, #ffffff);
    padding: 1.4rem 3rem;
    display: flex; gap: 2.5rem; align-items: center;
    border-bottom: 1px solid #e0f2fe;
}
.stat-item {
    display: flex;
    align-items: baseline;
    gap: 0.6rem;
    opacity: 0;
    animation: slideUpFade 0.6s ease forwards;
}
.stat-item:nth-child(1) { animation-delay: 0.1s; }
.stat-item:nth-child(3) { animation-delay: 0.25s; }
.stat-item:nth-child(5) { animation-delay: 0.4s; }

@keyframes slideUpFade {
    0%   { opacity: 0; transform: translateY(8px); }
    100% { opacity: 1; transform: translateY(0); }
}

.stat-n {
    font-size: 2rem;
    font-weight: 800;
    color: #0ea5e9;
    letter-spacing: -1.2px;
    display: inline-block;
}

/* Counter animé via CSS */
.stat-n.counter {
    animation: countUp 1.2s cubic-bezier(0.4, 0, 0.2, 1);
}
@keyframes countUp {
    0%   { transform: translateY(20px); opacity: 0; }
    60%  { opacity: 1; }
    100% { transform: translateY(0); opacity: 1; }
}

.stat-label-wrap { display: flex; flex-direction: column; }
.stat-l {
    font-size: 0.72rem;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}
.stat-sub { font-size: 0.68rem; color: #64748b; }
.stat-sep {
    width: 1px;
    height: 34px;
    background: #e2e8f0;
    flex-shrink: 0;
}

/* ═══════════════════════════════════════════════════
   MAIN
   ═══════════════════════════════════════════════════ */
.main-wrap { max-width: 1280px; margin: 0 auto; padding: 1.2rem 3rem 4rem; }

/* ═══════════════════════════════════════════════════
   SIDEBAR BOXES
   ═══════════════════════════════════════════════════ */
.sb-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.2rem 1.3rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.sb-box:hover {
    border-color: #7dd3fc;
    box-shadow: 0 4px 16px rgba(14,165,233,0.08);
}
.sb-title {
    font-size: 0.6rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #0ea5e9;
    margin-bottom: 0.7rem;
}
div[data-testid="stSelectbox"] > div > div {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
}
.main-wrap input[type="text"] {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
    font-size: 0.85rem !important;
}

/* ═══════════════════════════════════════════════════
   JOB CARDS — staggered reveal
   ═══════════════════════════════════════════════════ */
.job-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    overflow: hidden;
    display: flex;
    margin-bottom: 0.75rem;
    transition: transform 0.15s, box-shadow 0.15s, border-color 0.15s;
    opacity: 0;
    animation: cardReveal 0.5s ease forwards;
}
@keyframes cardReveal {
    0%   { opacity: 0; transform: translateY(12px); }
    100% { opacity: 1; transform: translateY(0); }
}
/* Staggered delay — les 20 premières cartes ont un délai progressif */
.job-card:nth-child(1)  { animation-delay: 0.05s; }
.job-card:nth-child(2)  { animation-delay: 0.10s; }
.job-card:nth-child(3)  { animation-delay: 0.15s; }
.job-card:nth-child(4)  { animation-delay: 0.20s; }
.job-card:nth-child(5)  { animation-delay: 0.25s; }
.job-card:nth-child(6)  { animation-delay: 0.30s; }
.job-card:nth-child(7)  { animation-delay: 0.35s; }
.job-card:nth-child(8)  { animation-delay: 0.40s; }
.job-card:nth-child(9)  { animation-delay: 0.45s; }
.job-card:nth-child(10) { animation-delay: 0.50s; }
.job-card:nth-child(11) { animation-delay: 0.55s; }
.job-card:nth-child(12) { animation-delay: 0.60s; }
.job-card:nth-child(13) { animation-delay: 0.65s; }
.job-card:nth-child(14) { animation-delay: 0.70s; }
.job-card:nth-child(15) { animation-delay: 0.75s; }
.job-card:nth-child(n+16) { animation-delay: 0.80s; }

.job-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(14,165,233,0.12);
    border-color: #7dd3fc;
}
.card-stripe { width: 4px; flex-shrink: 0; }
.s0{background:#0ea5e9;} .s1{background:#38bdf8;}
.s2{background:#0284c7;} .s3{background:#7dd3fc;} .s4{background:#0369a1;}
.card-content { padding: 1rem 1.3rem; flex:1; display:flex; align-items:center; gap:1rem; }
.card-main { flex: 1; }
.card-co {
    font-size:.62rem;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:1px;
    color:#0ea5e9;
    margin-bottom:.25rem;
}
.card-title {
    font-size:.95rem;
    font-weight:700;
    color:#0f172a;
    line-height:1.3;
    margin-bottom:.3rem;
}
.card-loc { font-size:.78rem; color:#64748b; }
.card-btn {
    background: transparent;
    color: #0ea5e9 !important;
    text-decoration: none;
    padding: .4rem .8rem;
    border-radius: 6px;
    font-size: .78rem;
    font-weight: 700;
    white-space: nowrap;
    transition: all .15s;
}
.card-btn:hover {
    color: #0284c7 !important;
    transform: translateX(3px);
}

/* ═══════════════════════════════════════════════════
   BAR CHART
   ═══════════════════════════════════════════════════ */
.chart-row { margin-bottom:.6rem; }
.chart-lbl {
    font-size:.7rem;
    color:#475569;
    margin-bottom:.25rem;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}
.chart-bg { background:#e0f2fe; border-radius:4px; height:5px; }
.chart-fill {
    height:5px;
    border-radius:4px;
    background: linear-gradient(to right, #0ea5e9, #38bdf8);
    animation: chartGrow 1s ease forwards;
    transform-origin: left;
    transform: scaleX(0);
}
@keyframes chartGrow {
    to { transform: scaleX(1); }
}

/* ═══════════════════════════════════════════════════
   EMPTY STATE — avec stats Adzuna
   ═══════════════════════════════════════════════════ */
.empty-wrap {
    text-align:center;
    padding: 1.5rem 2rem 4rem;
    max-width: 720px;
    margin: 0 auto;
}
.empty-ico {
    font-size: 3.2rem;
    margin-bottom: 1.2rem;
    display: block;
    animation: floaty 3s ease-in-out infinite;
}
@keyframes floaty {
    0%,100% { transform: translateY(0); }
    50%     { transform: translateY(-8px); }
}
.empty-t {
    font-size: 1.6rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: .5rem;
    letter-spacing: -.8px;
}
.empty-s {
    font-size: 0.95rem;
    color: #64748b;
    margin-bottom: 2.5rem;
}

/* Stats cards état vide */
.hero-stats {
    display: flex;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
    margin-top: 2rem;
}
.hero-stat-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.3rem 1.6rem;
    min-width: 180px;
    text-align: left;
    transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
}
.hero-stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(14,165,233,0.12);
    border-color: #7dd3fc;
}
.hero-stat-icon {
    font-size: 1.3rem;
    margin-bottom: 0.6rem;
    display: block;
}
.hero-stat-label {
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #0ea5e9;
    margin-bottom: 0.3rem;
}
.hero-stat-value {
    font-size: 1rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.3;
}

.section-t {
    font-size:.62rem;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:1.5px;
    color:#0ea5e9;
    margin-bottom:.8rem;
}

/* Hide labels outside form */
.main-wrap [data-testid="stWidgetLabel"] { display: none !important; }
.stTextInput, .stSelectbox, .stSlider { margin-bottom: 0 !important; }
div[data-testid="stSlider"] > div { padding: 0 !important; }

/* Download button — minimaliste bleu ciel */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: #0ea5e9 !important;
    border: none !important;
    border-radius: 6px !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    padding: 0.4rem 0.8rem !important;
    width: auto !important;
    transition: all 0.15s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    color: #0284c7 !important;
    background: transparent !important;
    transform: translateX(2px) !important;
}
[data-testid="stDownloadButton"] {
    display: flex !important;
    justify-content: flex-end !important;
    margin-bottom: 0.8rem !important;
}

/* Spinner Streamlit - couleur bleu ciel */
.stSpinner > div > div {
    border-top-color: #0ea5e9 !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────────────────
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "searched" not in st.session_state:
    st.session_state.searched = False

# ── NAVBAR ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div class="nav-logo">My<span>Ideal</span>Job</div>
  <div class="nav-pill"><div class="live-dot"></div>En direct · Marché belge</div>
</div>
""", unsafe_allow_html=True)

# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-inner">
    <div class="hero-h1">Trouvez votre<br><em>job idéal</em></div>
    <div class="hero-sub">Scrapez les offres du marché belge en temps réel &nbsp;·&nbsp; Filtrez &nbsp;·&nbsp; Exportez en CSV</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── SEARCH FORM ────────────────────────────────────────────────────────────────
with st.form("search_form"):
    c1, c2, c3, c4, c5 = st.columns([2.8, 2.8, 1.8, 1.8, 1.4])
    with c1:
        query = st.text_input(
            "INTITULÉ DU POSTE",
            placeholder="Ex: data analyst, comptable..."
        )
    with c2:
        location = st.text_input(
            "VILLE",
            placeholder="Ex: Bruxelles, Liège..."
        )
    with c3:
        max_jobs = st.slider("NOMBRE D'OFFRES", min_value=5, max_value=50, value=20)
    with c4:
        distance = st.slider("RAYON (KM)", min_value=0, max_value=100, value=25, step=5)
    with c5:
        st.markdown('<div style="padding-top:1.8rem;">', unsafe_allow_html=True)
        launch = st.form_submit_button("Rechercher →")
        st.markdown('</div>', unsafe_allow_html=True)

# ── SCRAPING ───────────────────────────────────────────────────────────────────
if launch and query:
    with st.spinner("Analyse du marché en cours..."):
        raw = scrape_indeed(query, location or "Belgique", max_jobs, distance)
        parsed = parse_jobs(raw)
        export_to_csv(parsed, filename="jobs_output.csv")
        st.session_state.jobs = parsed
        st.session_state.query = query
        st.session_state.searched = True

jobs = st.session_state.jobs
searched = st.session_state.searched

# ── STATS STRIP ────────────────────────────────────────────────────────────────
if searched and jobs:
    nb_co = len(set(j["entreprise"] for j in jobs))
    nb_ci = len(set(j["lieu"] for j in jobs))
    q = st.session_state.get("query", "")
    st.markdown(f"""
    <div class="stats-strip">
      <div class="stat-item">
        <div class="stat-n counter">{len(jobs)}</div>
        <div class="stat-label-wrap">
          <div class="stat-l">offres</div>
          <div class="stat-sub">trouvées</div>
        </div>
      </div>
      <div class="stat-sep"></div>
      <div class="stat-item">
        <div class="stat-n counter">{nb_co}</div>
        <div class="stat-label-wrap">
          <div class="stat-l">entreprises</div>
          <div class="stat-sub">différentes</div>
        </div>
      </div>
      <div class="stat-sep"></div>
      <div class="stat-item">
        <div class="stat-n counter">{nb_ci}</div>
        <div class="stat-label-wrap">
          <div class="stat-l">villes</div>
          <div class="stat-sub">couvertes</div>
        </div>
      </div>
      <div style="margin-left:auto;font-size:.85rem;color:#64748b;font-style:italic;">
        Résultats pour &nbsp;
        <span style="color:#0f172a;font-style:normal;font-weight:700;">"{q}"</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── MAIN ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

if not searched:
    # État vide avec stats Adzuna (Option A — chiffres figés honnêtes)
    st.markdown("""
    <div class="empty-wrap">
      <span class="empty-ico">🔍</span>
      <div class="empty-t">Prêt à scanner le marché</div>
      <div class="empty-s">Entrez un intitulé de poste et une ville, puis cliquez sur Rechercher</div>
      <div class="hero-stats">
        <div class="hero-stat-card">
          <span class="hero-stat-icon">🌍</span>
          <div class="hero-stat-label">Propulsé par</div>
          <div class="hero-stat-value">API Adzuna</div>
        </div>
        <div class="hero-stat-card">
          <span class="hero-stat-icon">📊</span>
          <div class="hero-stat-label">Offres indexées</div>
          <div class="hero-stat-value">1M+ en Europe</div>
        </div>
        <div class="hero-stat-card">
          <span class="hero-stat-icon">🇧🇪</span>
          <div class="hero-stat-label">Couverture</div>
          <div class="hero-stat-value">Belgique complète</div>
        </div>
        <div class="hero-stat-card">
          <span class="hero-stat-icon">⚡</span>
          <div class="hero-stat-label">Export</div>
          <div class="hero-stat-value">CSV instantané</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

elif not jobs:
    q = st.session_state.get("query", "")
    st.markdown(f"""
    <div class="empty-wrap">
      <span class="empty-ico">😕</span>
      <div class="empty-t">Aucune offre trouvée</div>
      <div class="empty-s">Pas de résultats pour <strong>"{q}"</strong>. Essayez un autre intitulé, une autre ville, ou augmentez le rayon.</div>
    </div>
    """, unsafe_allow_html=True)

else:
    df = pd.DataFrame(jobs)
    col_sb, col_main = st.columns([1, 3])

    with col_sb:
        st.markdown('<div class="sb-box"><div class="sb-title">Filtrer par titre</div>', unsafe_allow_html=True)
        search_text = st.text_input("Titre", placeholder="ex: senior, junior...", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-box"><div class="sb-title">Entreprise</div>', unsafe_allow_html=True)
        filtre_co = st.selectbox("Entreprise", ["Toutes"] + sorted(df["entreprise"].unique().tolist()), label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-box"><div class="sb-title">Ville</div>', unsafe_allow_html=True)
        filtre_lieu = st.selectbox("Ville", ["Tous"] + sorted(df["lieu"].unique().tolist()), label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        counts = df["entreprise"].value_counts().head(6)
        max_c = counts.max()
        chart_html = '<div class="sb-box"><div class="sb-title">Top entreprises</div>'
        for name, cnt in counts.items():
            pct = int(cnt / max_c * 100)
            chart_html += f'<div class="chart-row"><div class="chart-lbl">{name}</div><div class="chart-bg"><div class="chart-fill" style="width:{pct}%"></div></div></div>'
        chart_html += '</div>'
        st.markdown(chart_html, unsafe_allow_html=True)

    with col_main:
        df_f = df.copy()
        if filtre_co != "Toutes":
            df_f = df_f[df_f["entreprise"] == filtre_co]
        if filtre_lieu != "Tous":
            df_f = df_f[df_f["lieu"] == filtre_lieu]
        if search_text:
            df_f = df_f[df_f["titre"].str.contains(search_text, case=False, na=False)]

        n = len(df_f)
        
        header_c1, header_c2 = st.columns([3, 1])
        with header_c1:
            st.markdown(f'<div class="section-t" style="padding-top:.6rem;">{n} offre{"s" if n>1 else ""} trouvée{"s" if n>1 else ""}</div>', unsafe_allow_html=True)
        with header_c2:
            csv = df_f.to_csv(index=False).encode("utf-8-sig")
            st.download_button("⬇ Exporter CSV", data=csv, file_name="myidealjob.csv", mime="text/csv")

        colors = ["s0", "s1", "s2", "s3", "s4"]
        for i, (_, row) in enumerate(df_f.iterrows()):
            st.markdown(f"""
            <div class="job-card">
              <div class="card-stripe {colors[i % len(colors)]}"></div>
              <div class="card-content">
                <div class="card-main">
                  <div class="card-co">{row['entreprise']}</div>
                  <div class="card-title">{row['titre']}</div>
                  <div class="card-loc">📍 {row['lieu']}</div>
                </div>
                <a class="card-btn" href="{row['lien']}" target="_blank">Voir l'offre →</a>
              </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDER CSS OVERRIDE — injecté EN DERNIER (après le rendu Streamlit)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
div[data-testid="stSlider"] .e2ups023 {
    background: #0ea5e9 !important;
    border-radius: 4px !important;
}
div[data-testid="stSlider"] .e2ups024 {
    background: #0ea5e9 !important;
}
div[data-testid="stSlider"] .e2ups021 {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    width: 0 !important;
    height: 0 !important;
}
div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
    bottom: -0.05rem !important;
    position: absolute !important;
    transform: translateX(-50%) !important;
    opacity: 1 !important;
    visibility: visible !important;
    z-index: 10 !important;
    background: transparent !important;
}
div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] [data-testid="stMarkdownContainer"] {
    background: #0ea5e9 !important;
    border-radius: 50px !important;
    padding: 0.18rem 0.55rem !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-width: 28px !important;
    box-shadow: 0 0 0 3px rgba(14,165,233,0.25), 0 2px 8px rgba(14,165,233,0.35) !important;
    cursor: grab !important;
}
div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] p {
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 0.7rem !important;
    margin: 0 !important;
    line-height: 1 !important;
    background: transparent !important;
}
/* Force tick mark minimum (point noir au début) à disparaître ou être bleu */
div[data-testid="stSlider"] > div > div > div > div {
    background-color: #0ea5e9 !important;
}

/* ═══════════════════════════════════════════════════
   FIX CHIRURGICAL — segment noir sibling du rail
   HTML structure :
   <div class="st-ck st-cl ..."> (rail wrapper)
     <div class="e2ups023">...</div> (rail principal)
     <div class="st-au st-av st-aw st-ax st-cp st-cq st-b8 st-cr st-cs"></div> ← CE SEGMENT NOIR
   </div>
   Les classes st-au/st-av/st-cp/st-cq/st-cr/st-cs sont stables BaseWeb.
   On cible spécifiquement ce sibling.
   ═══════════════════════════════════════════════════ */
div[data-testid="stSlider"] .st-au.st-av.st-aw,
div[data-testid="stSlider"] .st-cp.st-cq.st-cr,
div[data-testid="stSlider"] div[class*="st-cp"][class*="st-cq"] {
    background: #0ea5e9 !important;
    background-color: #0ea5e9 !important;
}
/* Hide "Press Enter to submit form" */
[data-testid="InputInstructions"],
div[class*="InputInstructions"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    opacity: 0 !important;
    position: absolute !important;
    pointer-events: none !important;
}
</style>
""", unsafe_allow_html=True)
