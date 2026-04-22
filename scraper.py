import requests
import json
import sys
import os

try:
    import streamlit as st
    ADZUNA_APP_ID = st.secrets["ADZUNA_APP_ID"]
    ADZUNA_APP_KEY = st.secrets["ADZUNA_APP_KEY"]
except:
    from dotenv import load_dotenv
    load_dotenv()
    ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
    ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")


def scrape_indeed(query: str, location: str, max_jobs: int = 20) -> list[dict]:
    url = "https://api.adzuna.com/v1/api/jobs/be/search/1"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": query,
        "where": location,
        "results_per_page": max_jobs,
        "content-type": "application/json"
    }

    jobs = []

    try:
        response = requests.get(url, params=params, timeout=15)
        data = response.json()
        results = data.get("results", [])

        for job in results:
            jobs.append({
                "titre": job.get("title", "N/A"),
                "entreprise": job.get("company", {}).get("display_name", "N/A"),
                "lieu": job.get("location", {}).get("display_name", "N/A"),
                "lien": job.get("redirect_url", "N/A"),
                "query": query,
                "location": location,
            })
    except Exception as e:
        print(f"Erreur API : {e}")

    return jobs


if __name__ == "__main__":
    if len(sys.argv) == 4:
        query = sys.argv[1]
        location = sys.argv[2]
        max_jobs = int(sys.argv[3])
        results = scrape_indeed(query, location, max_jobs)
        sys.stdout.write(json.dumps(results))
        sys.stdout.flush()
    else:
        results = scrape_indeed("data analyst", "Bruxelles", max_jobs=5)
        for job in results:
            print(job)
            