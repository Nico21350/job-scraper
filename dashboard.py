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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');

html, body, [class*="css"], [class*="st-"] {
    font-family: 'Inter', sans-serif !important;
}

/* Cache tout le chrome Streamlit */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { 
    visibility: hidden !important; display: none !important;
}

/* Reset padding */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Background global */
.stApp { background: #f7f7f5 !important; }

/* ---- NAVBAR ---- */
.navbar {
    background: white;
    border-bottom: 1px solid #e5e5e5;
    padding: 0 2.5rem;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
}
.nav-logo { font-size: 1.2rem; font-weight: 900; color: #111; }
.nav-logo span { color: #2563eb; }
.nav-right { display: flex; align-items: center; gap: 1rem; font-size: 0.78rem; }
.nav-live { color: #16a34a; font-weight: 600; display: flex; align-items: center; gap: 0.4rem; }
.nav-badge { background: #f0f0ee; border-radius: 20px; padding: 0.25rem 0.75rem; color: #666; font-weight: 600; }

/* ---- HERO ---- */
.hero-wrap {
    background: white;
    border-bottom: 1px solid #e5e5e5;
    padding: 3rem 2.5rem 2.5rem;
}
.hero-inner { max-width: 900px; }
.hero-h1 {
    font-size: 3rem; font-weight: 900;
    letter-spacing: -2px; line-height: 1.05;
    color: #111; margin-bottom: 0.5rem;
}
.hero-h1 em { font-style: normal; color: #2563eb; }
.hero-sub { font-size: 0.95rem; color: #888; line-height: 1.6; margin-bottom: 1.5rem; }

/* ---- SEARCH BAR ---- */
.search-wrap {
    background: #f7f7f5;
    border: 1.5px solid #e0e0e0;
    border-radius: 14px;
    padding: 0.5rem 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    max-width: 800px;
    margin-bottom: 0.5rem;
}
.search-label {
    font-size: 0.65rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1.5px;
    color: #aaa; white-space: nowrap;
}
.search-divider { width: 1px; height: 28px; background: #e0e0e0; }

/* Override Streamlit inputs dans le hero */
.hero-inputs div[data-testid="stTextInput"] input {
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    padding: 0.3rem 0 !important;
    font-size: 0.95rem !important;
    font-family: 'Inter', sans-serif !important;
}
.hero-inputs div[data-testid="stTextInput"] > div {
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
}
.hero-inputs .stSlider { padding-top: 0 !important; }
.hero-inputs [data-testid="stSlider"] { padding: 0 !important; }

/* Bouton recherche */
.stButton > button {
    background: #111 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1.5rem !important;
    width: 100% !important;
    transition: background 0.2s !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    background: #2563eb !important;
}

/* ---- STATS ---- */
.stats-row {
    display: flex; gap: 1rem; flex-wrap: wrap;
    margin-top: 1.5rem;
}
.stat-box {
    background: #f7f7f5; border: 1px solid #e5e5e5;
    border-radius: 12px; padding: 1rem 1.4rem;
    min-width: 120px;
    transition: transform 0.2s;
}
.stat-box:hover { transform: translateY(-2px); }
.stat-n { font-size: 2rem; font-weight: 900; letter-spacing: -1px; color: #111; }
.stat-n.blue { color: #2563eb; }
.stat-l { font-size: 0.62rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #bbb; }

/* ---- LAYOUT PRINCIPAL ---- */
.main-wrap {
    max-width: 1300px;
    margin: 0 auto;
    padding: 2rem 2.5rem 4rem;
}

/* ---- SIDEBAR FILTRES ---- */
.sidebar-box {
    background: white;
    border: 1px solid #e5e5e5;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}
.sidebar-t {
    font-size: 0.62rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1.5px;
    color: #bbb; margin-bottom: 0.7rem;
}

/* Selectbox */
div[data-testid="stSelectbox"] > div > div {
    background: #f7f7f5 !important;
    border: 1px solid #e5e5e5 !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
}

/* TextInput dans filtres */
div[data-testid="stTextInput"] input {
    background: #f7f7f5 !important;
    border: 1px solid #e5e5e5 !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
}

/* ---- CARDS ---- */
.job-card {
    background: white;
    border: 1px solid #e5e5e5;
    border-radius: 14px;
    overflow: hidden;
    display: flex;
    margin-bottom: 0.8rem;
    transition: transform 0.18s, box-shadow 0.18s;
}
.job-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.09);
}
.card-stripe { width: 5px; flex-shrink: 0; }
.s0 { background: #2563eb; }
.s1 { background: #16a34a; }
.s2 { background: #7c3aed; }
.s3 { background: #ea580c; }
.s4 { background: #0891b2; }
.card-content { padding: 1rem 1.3rem; flex: 1; }
.card-co { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #bbb; margin-bottom: 0.2rem; }
.card-title { font-size: 0.95rem; font-weight: 700; color: #111; margin-bottom: 0.5rem; line-height: 1.3; }
.card-foot { display: flex; align-items: center; justify-content: space-between; }
.card-loc { font-size: 0.78rem; color: #888; }
.card-btn {
    background: #111; color: white;
    text-decoration: none; padding: 0.28rem 0.8rem;
    border-radius: 20px; font-size: 0.7rem; font-weight: 700;
    transition: background 0.18s;
}
.card-btn:hover { background: #2563eb; color: white; }

/* ---- CHART ---- */
.chart-row { margin-bottom: 0.5rem; }
.chart-lbl { font-size: 0.7rem; color: #555; margin-bottom: 0.2rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.chart-bg { background: #f0f0ee; border-radius: 4px; height: 5px; }
.chart-fill { height: 5px; border-radius: 4px; background: linear-gradient(90deg, #2563eb, #60a5fa); }

/* ---- EMPTY STATE ---- */
.empty-wrap { text-align: center; padding: 5rem 2rem; }
.empty-ico { font-size: 2.5rem; margin-bottom: 1rem; }
.empty-t { font-size: 1.2rem; font-weight: 900; color: #333; margin-bottom: 0.4rem; }
.empty-s { font-size: 0.85rem; color: #bbb; }

/* ---- SECTION TITLES ---- */
.section-t {
    font-size: 0.65rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1.5px;
    color: #bbb; margin-bottom: 0.8rem;
}

/* Remove streamlit label spacing */
[data-testid="stWidgetLabel"] { display: none !important; }
.stTextInput, .stSelectbox, .stSlider { margin-bottom: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ---- STATE ----
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "searched" not in st.session_state:
    st.session_state.searched = False

# ---- NAVBAR ----
st.markdown("""
<div class="navbar">
  <div class="nav-logo">My<span>Ideal</span>Job</div>
  <div class="nav-right">
    <div class="nav-live">● En direct</div>
    <div class="nav-badge">🇧🇪 Marché belge</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---- HERO + SEARCH ----
st.markdown("""
<div class="hero-wrap">
  <div class="hero-inner">
    <div class="hero-h1">Trouvez votre<br><em>job idéal.</em></div>
    <div class="hero-sub">Scrapez les offres du marché belge en temps réel · Filtrez · Exportez</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Barre de recherche dans le hero
with st.container():
    st.markdown('<div style="background:white;padding:0 2.5rem 2rem;border-bottom:1px solid #e5e5e5;">', unsafe_allow_html=True)
    with st.form("search_form"):
        c1, c2, c3, c4 = st.columns([4, 4, 3, 1])
        with c1:
            st.markdown('<div style="font-size:0.62rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:#aaa;margin-bottom:0.2rem;">Intitulé du poste</div>', unsafe_allow_html=True)
            query = st.text_input("Poste", placeholder="Ex: data analyst, comptable...", label_visibility="collapsed")
        with c2:
            st.markdown('<div style="font-size:0.62rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:#aaa;margin-bottom:0.2rem;">Ville</div>', unsafe_allow_html=True)
            location = st.text_input("Ville", placeholder="Ex: Bruxelles, Liège...", label_visibility="collapsed")
        with c3:
            st.markdown('<div style="font-size:0.62rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:#aaa;margin-bottom:0.2rem;">Nombre d\'offres</div>', unsafe_allow_html=True)
            max_jobs = st.slider("Offres", 5, 50, 20, label_visibility="collapsed")
        with c4:
            st.markdown('<div style="margin-top:1.4rem;">', unsafe_allow_html=True)
            launch = st.form_submit_button("🔍 Go")
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---- SCRAPING ----
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

# ---- STATS ----
if searched and jobs:
    nb_co = len(set(j["entreprise"] for j in jobs))
    nb_ci = len(set(j["lieu"] for j in jobs))
    q = st.session_state.get("query", "")
    st.markdown(f"""
    <div style="background:white;padding:1.2rem 2.5rem;border-bottom:1px solid #e5e5e5;">
      <div class="stats-row">
        <div class="stat-box"><div class="stat-n blue">{len(jobs)}</div><div class="stat-l">Offres trouvées</div></div>
        <div class="stat-box"><div class="stat-n">{nb_co}</div><div class="stat-l">Entreprises</div></div>
        <div class="stat-box"><div class="stat-n">{nb_ci}</div><div class="stat-l">Villes</div></div>
        <div class="stat-box"><div class="stat-n" style="font-size:1rem;margin-top:0.4rem">{q}</div><div class="stat-l">Recherche</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ---- MAIN LAYOUT ----
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

if not searched:
    st.markdown("""
    <div class="empty-wrap">
      <div class="empty-ico">🔍</div>
      <div class="empty-t">Prêt à scanner le marché</div>
      <div class="empty-s">Entrez un intitulé de poste et une ville puis cliquez sur Go</div>
    </div>
    """, unsafe_allow_html=True)
else:
    df = pd.DataFrame(jobs)
    col_sidebar, col_main = st.columns([1, 3])

    with col_sidebar:
        # Filtre titre
        st.markdown('<div class="sidebar-box"><div class="sidebar-t">Filtrer par titre</div>', unsafe_allow_html=True)
        search_text = st.text_input("Titre", placeholder="Ex: senior, junior...", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        # Filtre entreprise
        st.markdown('<div class="sidebar-box"><div class="sidebar-t">Entreprise</div>', unsafe_allow_html=True)
        entreprises = ["Toutes"] + sorted(df["entreprise"].unique().tolist())
        filtre_co = st.selectbox("Entreprise", entreprises, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        # Filtre ville
        st.markdown('<div class="sidebar-box"><div class="sidebar-t">Ville</div>', unsafe_allow_html=True)
        lieux = ["Tous"] + sorted(df["lieu"].unique().tolist())
        filtre_lieu = st.selectbox("Ville", lieux, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        # Chart top entreprises
        counts = df["entreprise"].value_counts().head(6)
        max_c = counts.max()
        chart_html = '<div class="sidebar-box"><div class="sidebar-t">Top entreprises</div>'
        for name, cnt in counts.items():
            pct = int(cnt / max_c * 100)
            chart_html += f'<div class="chart-row"><div class="chart-lbl" title="{name}">{name}</div><div class="chart-bg"><div class="chart-fill" style="width:{pct}%"></div></div></div>'
        chart_html += '</div>'
        st.markdown(chart_html, unsafe_allow_html=True)

        # Export
        df_exp = df.copy()
        csv = df_exp.to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇ Exporter CSV", data=csv, file_name="myidealjob_export.csv", mime="text/csv")

    with col_main:
        # Appliquer filtres
        df_f = df.copy()
        if filtre_co != "Toutes":
            df_f = df_f[df_f["entreprise"] == filtre_co]
        if filtre_lieu != "Tous":
            df_f = df_f[df_f["lieu"] == filtre_lieu]
        if search_text:
            df_f = df_f[df_f["titre"].str.contains(search_text, case=False, na=False)]

        st.markdown(f'<div class="section-t">{len(df_f)} offre{"s" if len(df_f) > 1 else ""}</div>', unsafe_allow_html=True)

        colors = ["s0", "s1", "s2", "s3", "s4"]
        for i, (_, row) in enumerate(df_f.iterrows()):
            st.markdown(f"""
            <div class="job-card">
              <div class="card-stripe {colors[i % len(colors)]}"></div>
              <div class="card-content">
                <div class="card-co">{row['entreprise']}</div>
                <div class="card-title">{row['titre']}</div>
                <div class="card-foot">
                  <div class="card-loc">📍 {row['lieu']}</div>
                  <a class="card-btn" href="{row['lien']}" target="_blank">Voir l'offre →</a>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
