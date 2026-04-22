# parser.py — nettoyage et structuration des offres

from datetime import datetime


def clean_text(text: str) -> str:
    """Nettoie un texte brut."""
    if not text or text == "N/A":
        return "N/A"
    return " ".join(text.split())


def parse_jobs(raw_jobs: list[dict]) -> list[dict]:
    """Nettoie et structure une liste d'offres brutes."""
    
    parsed = []
    seen_links = set()  # Pour dédoublonner
    
    for job in raw_jobs:
        link = job.get("lien", "N/A")
        
        # Dédoublonnage par lien
        if link in seen_links:
            continue
        seen_links.add(link)
        
        parsed.append({
            "titre":      clean_text(job.get("titre", "N/A")),
            "entreprise": clean_text(job.get("entreprise", "N/A")),
            "lieu":       clean_text(job.get("lieu", "N/A")),
            "lien":       link,
            "query":      job.get("query", "N/A"),
            "location":   job.get("location", "N/A"),
            "date_scrape": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
    
    print(f"  → {len(parsed)} offres après nettoyage (/{len(raw_jobs)} brutes)")
    return parsed


if __name__ == "__main__":
    # Test avec des données fictives
    test_data = [
        {"titre": "  Data Analyst  ", "entreprise": "BNP Paribas", "lieu": "Bruxelles", "lien": "https://example.com/1", "query": "data analyst", "location": "Bruxelles"},
        {"titre": "Data Analyst", "entreprise": "BNP Paribas", "lieu": "Bruxelles", "lien": "https://example.com/1", "query": "data analyst", "location": "Bruxelles"},  # doublon
        {"titre": "Python Dev", "entreprise": "Extia", "lieu": "N/A", "lien": "https://example.com/2", "query": "python", "location": "Bruxelles"},
    ]
    
    results = parse_jobs(test_data)
    for job in results:
        print(job)
        