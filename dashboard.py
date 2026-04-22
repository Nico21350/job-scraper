import streamlit as st
import pandas as pd
import subprocess
import json
import sys
from parser import parse_jobs
from exporter import export_to_csv

st.set_page_config(page_title="Job Scraper — RPA Demo", page_icon="🔍", layout="wide")
st.title("🔍 Job Scraper — RPA Demo")
st.markdown("Scrape les offres d'emploi sur Indeed BE en temps réel.")

st.sidebar.header("Paramètres de recherche")
query = st.sidebar.text_input("Mot-clé", value="data analyst")
location = st.sidebar.text_input("Localisation", value="Bruxelles")
max_jobs = st.sidebar.slider("Nombre max d'offres", 5, 50, 20)
launch = st.sidebar.button("🚀 Lancer le scraping", use_container_width=True)

if launch:
    with st.spinner(f"Scraping '{query}' @ {location}..."):
        result = subprocess.run(
            [sys.executable, "scraper.py", query, location, str(max_jobs)],
            capture_output=True, text=True
        )
        try:
            raw = json.loads(result.stdout)
        except:
            raw = []
        parsed = parse_jobs(raw)
        export_to_csv(parsed, filename="jobs_output.csv")
    st.success(f"{len(parsed)} offres trouvées et exportées ✓")
    st.session_state["jobs"] = parsed

if "jobs" in st.session_state and len(st.session_state["jobs"]) > 0:
    jobs = st.session_state["jobs"]
    df = pd.DataFrame(jobs)

    st.subheader("Filtres")
    col1, col2 = st.columns(2)
    with col1:
        entreprises = ["Toutes"] + sorted(df["entreprise"].unique().tolist())
        filtre_entreprise = st.selectbox("Entreprise", entreprises)
    with col2:
        lieux = ["Tous"] + sorted(df["lieu"].unique().tolist())
        filtre_lieu = st.selectbox("Lieu", lieux)

    if filtre_entreprise != "Toutes":
        df = df[df["entreprise"] == filtre_entreprise]
    if filtre_lieu != "Tous":
        df = df[df["lieu"] == filtre_lieu]

    st.subheader(f"{len(df)} offres")
    st.dataframe(df[["titre", "entreprise", "lieu", "date_scrape"]], use_container_width=True, hide_index=True)

    st.subheader("Détail des offres")
    for _, row in df.iterrows():
        with st.expander(f"{row['titre']} — {row['entreprise']}"):
            st.write(f"📍 {row['lieu']}")
            st.write(f"🔗 [Voir l'offre]({row['lien']})")
            st.write(f"🕐 Scrapé le {row['date_scrape']}")

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(label="⬇️ Télécharger CSV", data=csv, file_name="jobs_export.csv", mime="text/csv")

elif not launch:
    st.info("Configure ta recherche dans la barre gauche et clique sur 'Lancer le scraping'.")