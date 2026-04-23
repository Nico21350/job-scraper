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
.stApp { background: #f4f3ee !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }

/* ── NAVBAR ── */
.navbar {
    background: #111;
    padding: 0 3rem;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.nav-logo { font-size: 1.15rem; font-weight: 800; color: white; letter-spacing: -0.3px; }
.nav-logo span { color: #a78bfa; }
.nav-pill {
    background: rgba(255,255,255,0.1);
    border-radius: 20px; padding: 0.25rem 0.9rem;
    font-size: 0.72rem; font-weight: 600; color: rgba(255,255,255,0.7);
    display: flex; align-items: center; gap: 0.4rem;
}
.live-dot {
    width: 6px; height: 6px; background: #4ade80;
    border-radius: 50%; animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:0.4; transform:scale(1.4); }
}

/* ── HERO ── */
.hero-wrap {
    background: #111;
    padding: 3rem 3rem 2rem;
}
.hero-h1 {
    font-size: 3.8rem; font-weight: 800;
    letter-spacing: -2.5px; line-height: 1.02;
    color: white; margin: 0 0 0.5rem;
}
.hero-h1 em { font-style: normal; color: #a78bfa; }
.hero-sub {
    font-size: 0.92rem; color: rgba(255,255,255,0.5);
    line-height: 1.6; margin: 0; white-space: nowrap;
}

/* ── FORM — dark bg, no border ── */
[data-testid="stForm"] {
    background: #111 !important;
    border: none !important;
    box-shadow: none !important;
    padding: 2rem 3rem 2.5rem !important;
    margin: 0 !important;
    border-bottom: 1px solid #2a2a2a !important;
}

/* ── NATIVE STREAMLIT LABELS — styled white/uppercase inside form ── */
[data-testid="stForm"] [data-testid="stWidgetLabel"] {
    display: block !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    color: rgba(255,255,255,0.35) !important;
    margin-bottom: 0.3rem !important;
}
[data-testid="stForm"] [data-testid="stWidgetLabel"] p {
    font-size: 0.6rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    color: rgba(255,255,255,0.35) !important;
    margin: 0 !important;
}

/* ── TEXT INPUTS inside form — dark ── */
[data-testid="stForm"] input[type="text"] {
    background: #1e1e1e !important;
    border: 1px solid #333 !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-size: 0.9rem !important;
}
[data-testid="stForm"] input[type="text"]::placeholder {
    color: rgba(255,255,255,0.3) !important;
}
[data-testid="stForm"] div[data-baseweb="input"] {
    background: #1e1e1e !important;
    border: 1px solid #333 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}
[data-testid="stForm"] div[data-baseweb="input"]:focus-within {
    border-color: #a78bfa !important;
}

/* ══════════════════════════════════════════════════════════
   SLIDER — thumb = étiquette, rail 100% violet
   ══════════════════════════════════════════════════════════ */

/* Rail complet — même couleur que la fill active, pas d'opacité */
div[data-testid="stSlider"] .e2ups023,
[data-testid="stForm"] div[data-testid="stSlider"] .e2ups023 {
    background: #a78bfa !important;
    border-radius: 4px !important;
}

/* Fill active — identique au rail (seamless) */
div[data-testid="stSlider"] .e2ups024,
[data-testid="stForm"] div[data-testid="stSlider"] .e2ups024 {
    background: #a78bfa !important;
}

/* Thumb cercle — transparent + pas de bordure visible :
   l'étiquette flottante LE remplace visuellement */
div[data-testid="stSlider"] .e2ups021,
[data-testid="stForm"] div[data-testid="stSlider"] .e2ups021 {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    width: 0 !important;
    height: 0 !important;
}

/* Étiquette positionnée SUR le rail, centrée sur le thumb,
   ressemble à un bouton/curseur — remplace le rond */
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

/* Le container markdown devient le "thumb" visuel */
div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] [data-testid="stMarkdownContainer"],
[data-testid="stForm"] div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] [data-testid="stMarkdownContainer"] {
    background: #a78bfa !important;
    border-radius: 50px !important;
    padding: 0.18rem 0.55rem !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: fit-content !important;
    min-width: 28px !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.35), 0 2px 6px rgba(0,0,0,0.3) !important;
    cursor: grab !important;
}

div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] p,
[data-testid="stForm"] div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] p {
    color: #111 !important;
    font-weight: 800 !important;
    font-size: 0.7rem !important;
    margin: 0 !important;
    line-height: 1 !important;
    background: transparent !important;
}

/* Tickbar — transparent, texte mauve */
div[data-testid="stSlider"] [data-testid="stSliderTickBar"],
div[data-testid="stSlider"] [data-testid="stSliderTickBar"] * {
    background: transparent !important;
    background-color: transparent !important;
    opacity: 1 !important;
    visibility: visible !important;
    box-shadow: none !important;
}
div[data-testid="stSlider"] [data-testid="stSliderTickBar"] p {
    color: #a78bfa !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
}

/* ══════════════════════════════════════════════════════════ */

/* ── BUTTON — violet ── */
[data-testid="stForm"] button,
.stButton > button {
    background: #a78bfa !important;
    color: #111 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
    padding: 0.65rem 1.4rem !important;
    width: 100% !important;
    white-space: nowrap !important;
    transition: background 0.2s !important;
}
[data-testid="stForm"] button:hover,
.stButton > button:hover { background: #c4b5fd !important; }

/* ── STATS STRIP ── */
.stats-strip {
    background: #111;
    padding: 1.1rem 3rem;
    display: flex; gap: 2rem; align-items: center;
    border-bottom: 1px solid #222;
}
.stat-item { display: flex; align-items: baseline; gap: 0.5rem; }
.stat-n { font-size: 1.8rem; font-weight: 800; color: #a78bfa; letter-spacing: -1px; }
.stat-label-wrap { display: flex; flex-direction: column; }
.stat-l { font-size: 0.7rem; font-weight: 700; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 1px; }
.stat-sub { font-size: 0.62rem; color: rgba(255,255,255,0.2); }
.stat-sep { width: 1px; height: 30px; background: rgba(255,255,255,0.1); flex-shrink: 0; }

/* ── MAIN ── */
.main-wrap { max-width: 1280px; margin: 0 auto; padding: 2rem 3rem 4rem; }

/* ── SIDEBAR BOXES ── */
.sb-box {
    background: white; border: 1px solid #e8e6e0;
    border-radius: 14px; padding: 1.2rem 1.3rem; margin-bottom: 0.8rem;
}
.sb-title {
    font-size: 0.6rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; color: #aaa; margin-bottom: 0.7rem;
}
div[data-testid="stSelectbox"] > div > div {
    background: #f4f3ee !important;
    border: 1px solid #e0ddd6 !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
}
/* Sidebar text inputs — beige (outside form) */
.main-wrap input[type="text"] {
    background: #f4f3ee !important;
    border: 1px solid #e0ddd6 !important;
    border-radius: 8px !important;
    color: #111 !important;
    font-size: 0.85rem !important;
}

/* ── JOB CARDS ── */
.job-card {
    background: white; border: 1px solid #e8e6e0;
    border-radius: 16px; overflow: hidden;
    display: flex; margin-bottom: 0.75rem;
    transition: transform 0.15s, box-shadow 0.15s;
}
.job-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.07); }
.card-stripe { width: 4px; flex-shrink: 0; }
.s0{background:#a78bfa;} .s1{background:#34d399;}
.s2{background:#60a5fa;} .s3{background:#fb923c;} .s4{background:#f472b6;}
.card-content { padding: 1rem 1.3rem; flex:1; display:flex; align-items:center; gap:1rem; }
.card-main { flex: 1; }
.card-co { font-size:.62rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:#aaa; margin-bottom:.2rem; }
.card-title { font-size:.95rem; font-weight:700; color:#111; line-height:1.3; margin-bottom:.3rem; }
.card-loc { font-size:.78rem; color:#888; }
.card-btn {
    background:#111; color:white !important; text-decoration:none;
    padding:.4rem 1rem; border-radius:20px; font-size:.72rem;
    font-weight:700; white-space:nowrap; transition:background .15s;
}
.card-btn:hover { background:#a78bfa; color:#111 !important; }

/* ── BAR CHART ── */
.chart-row { margin-bottom:.6rem; }
.chart-lbl { font-size:.7rem; color:#666; margin-bottom:.25rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.chart-bg { background:#f0ede6; border-radius:4px; height:5px; }
.chart-fill { height:5px; border-radius:4px; background:#a78bfa; }

/* ── EMPTY STATE ── */
.empty-wrap { text-align:center; padding:6rem 2rem; }
.empty-ico { font-size:3rem; margin-bottom:1rem; display:block; }
.empty-t { font-size:1.4rem; font-weight:800; color:#222; margin-bottom:.5rem; letter-spacing:-.5px; }
.empty-s { font-size:.9rem; color:#aaa; }

.section-t { font-size:.62rem; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; color:#aaa; margin-bottom:.8rem; }

/* Hide labels OUTSIDE form (sidebar filters) */
.main-wrap [data-testid="stWidgetLabel"] { display: none !important; }
.stTextInput, .stSelectbox, .stSlider { margin-bottom: 0 !important; }
div[data-testid="stSlider"] > div { padding: 0 !important; }

[data-testid="stDownloadButton"] > button {
    background: #111 !important; color: white !important;
    border: 1px solid #333 !important; border-radius: 8px !important;
    font-size: .8rem !important; font-weight: 600 !important; width: 100% !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #a78bfa !important; color: #111 !important; border-color: #a78bfa !important;
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
  <div class="hero-h1">Trouvez votre<br><em>job idéal.</em></div>
  <div class="hero-sub">Scrapez les offres du marché belge en temps réel &nbsp;·&nbsp; Filtrez &nbsp;·&nbsp; Exportez en CSV</div>
</div>
""", unsafe_allow_html=True)

# ── SEARCH FORM ────────────────────────────────────────────────────────────────
with st.form("search_form"):
    c1, c2, c3, c4 = st.columns([3, 3, 2, 1.4])
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
        st.markdown('<div style="padding-top:1.8rem;">', unsafe_allow_html=True)
        launch = st.form_submit_button("Rechercher →")
        st.markdown('</div>', unsafe_allow_html=True)

# ── SCRAPING ───────────────────────────────────────────────────────────────────
if launch and query:
    with st.spinner("Analyse du marché en cours..."):
        raw = scrape_indeed(query, location or "Belgique", max_jobs)
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
        <div class="stat-n">{len(jobs)}</div>
        <div class="stat-label-wrap">
          <div class="stat-l">offres</div>
          <div class="stat-sub">trouvées</div>
        </div>
      </div>
      <div class="stat-sep"></div>
      <div class="stat-item">
        <div class="stat-n">{nb_co}</div>
        <div class="stat-label-wrap">
          <div class="stat-l">entreprises</div>
          <div class="stat-sub">différentes</div>
        </div>
      </div>
      <div class="stat-sep"></div>
      <div class="stat-item">
        <div class="stat-n">{nb_ci}</div>
        <div class="stat-label-wrap">
          <div class="stat-l">villes</div>
          <div class="stat-sub">couvertes</div>
        </div>
      </div>
      <div style="margin-left:auto;font-size:.8rem;color:rgba(255,255,255,0.3);font-style:italic;">
        Résultats pour &nbsp;
        <span style="color:rgba(255,255,255,0.65);font-style:normal;font-weight:700;">"{q}"</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── MAIN ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

if not searched:
    st.markdown("""
    <div class="empty-wrap">
      <span class="empty-ico">🔍</span>
      <div class="empty-t">Prêt à scanner le marché</div>
      <div class="empty-s">Entrez un intitulé de poste et une ville, puis cliquez sur Rechercher</div>
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

        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇ Exporter CSV", data=csv, file_name="myidealjob.csv", mime="text/csv")

    with col_main:
        df_f = df.copy()
        if filtre_co != "Toutes":
            df_f = df_f[df_f["entreprise"] == filtre_co]
        if filtre_lieu != "Tous":
            df_f = df_f[df_f["lieu"] == filtre_lieu]
        if search_text:
            df_f = df_f[df_f["titre"].str.contains(search_text, case=False, na=False)]

        n = len(df_f)
        st.markdown(f'<div class="section-t">{n} offre{"s" if n>1 else ""} trouvée{"s" if n>1 else ""}</div>', unsafe_allow_html=True)

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
/* Rail = couleur pleine, pas de gap */
div[data-testid="stSlider"] .e2ups023 {
    background: #a78bfa !important;
    border-radius: 4px !important;
}
div[data-testid="stSlider"] .e2ups024 {
    background: #a78bfa !important;
}

/* Thumb invisible — remplacé par l étiquette */
div[data-testid="stSlider"] .e2ups021 {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    width: 0 !important;
    height: 0 !important;
}

/* Etiquette = nouveau thumb, positionne sur le rail */
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
    background: #a78bfa !important;
    border-radius: 50px !important;
    padding: 0.18rem 0.55rem !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-width: 28px !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.35), 0 2px 6px rgba(0,0,0,0.3) !important;
    cursor: grab !important;
}
div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] p {
    color: #111 !important;
    font-weight: 800 !important;
    font-size: 0.7rem !important;
    margin: 0 !important;
    line-height: 1 !important;
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)
