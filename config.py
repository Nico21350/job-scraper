# config.py — paramètres centralisés du job scraper

SEARCH_QUERIES = [
    "data analyst",
    "python developer",
    "automatisation RPA",
]

LOCATIONS = [
    "Bruxelles",
    "Belgique",
]

SOURCES = {
    "indeed": "https://be.indeed.com/jobs?q={query}&l={location}&lang=fr",
}

# Nombre max d'offres à scraper par recherche
MAX_JOBS_PER_QUERY = 20

# Délai entre les requêtes (secondes) — évite de se faire bloquer
REQUEST_DELAY = 2

# Fichier output
OUTPUT_FILE = "jobs_output.csv"
