# exporter.py — sauvegarde des offres en CSV

import csv
import os
from config import OUTPUT_FILE


def export_to_csv(jobs: list[dict], filename: str = OUTPUT_FILE) -> None:
    """Exporte une liste d'offres dans un fichier CSV."""
    
    if not jobs:
        print("  Aucune offre à exporter.")
        return
    
    file_exists = os.path.exists(filename)
    
    with open(filename, mode="a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
        
        # Écrire l'en-tête seulement si le fichier est nouveau
        if not file_exists:
            writer.writeheader()
        
        writer.writerows(jobs)
    
    print(f"  → {len(jobs)} offres exportées dans '{filename}'")


if __name__ == "__main__":
    test_data = [
        {"titre": "Data Analyst", "entreprise": "BNP Paribas", "lieu": "Bruxelles", "lien": "https://example.com/1", "query": "data analyst", "location": "Bruxelles", "date_scrape": "2026-04-21 10:25"},
        {"titre": "Python Dev", "entreprise": "Extia", "lieu": "Auderghem", "lien": "https://example.com/2", "query": "python", "location": "Bruxelles", "date_scrape": "2026-04-21 10:25"},
    ]
    
    export_to_csv(test_data)
    print("Fichier créé : jobs_output.csv")
    