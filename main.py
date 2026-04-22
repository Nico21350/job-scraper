# main.py — point d'entrée, orchestre tous les modules

from config import SEARCH_QUERIES, LOCATIONS, MAX_JOBS_PER_QUERY
from scraper import scrape_indeed
from parser import parse_jobs
from exporter import export_to_csv
import os


def run():
    print("=" * 50)
    print("JOB SCRAPER — Démarrage")
    print("=" * 50)

    # Supprime l'ancien CSV pour repartir propre
    if os.path.exists("jobs_output.csv"):
        os.remove("jobs_output.csv")
        print("Ancien fichier supprimé.\n")

    all_jobs = []

    for query in SEARCH_QUERIES:
        for location in LOCATIONS:
            print(f"\nRecherche : '{query}' @ {location}")
            raw = scrape_indeed(query, location, max_jobs=MAX_JOBS_PER_QUERY)
            parsed = parse_jobs(raw)
            all_jobs.extend(parsed)

    print(f"\n{'=' * 50}")
    print(f"TOTAL : {len(all_jobs)} offres collectées")
    export_to_csv(all_jobs)
    print("Terminé. Ouvre jobs_output.csv pour voir les résultats.")
    print("=" * 50)


if __name__ == "__main__":
    run()
    