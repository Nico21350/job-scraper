# scraper.py — navigation et extraction avec Playwright

import time
from playwright.sync_api import sync_playwright
from config import SOURCES, REQUEST_DELAY


def scrape_indeed(query: str, location: str, max_jobs: int = 20) -> list[dict]:
    """Scrape les offres Indeed pour une recherche donnée."""
    
    url = SOURCES["indeed"].format(
        query=query.replace(" ", "+"),
        location=location.replace(" ", "+")
    )
    
    jobs = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # False = on voit le navigateur
        page = browser.new_page()
        
        # Headers pour ne pas se faire bloquer
        page.set_extra_http_headers({
            "Accept-Language": "fr-BE,fr;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
        print(f"Scraping: {query} | {location}")
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(REQUEST_DELAY)
        
        # Extraction des offres
        cards = page.query_selector_all("div.job_seen_beacon")
        print(f"  → {len(cards)} offres trouvées")
        
        for card in cards[:max_jobs]:
            try:
                title = card.query_selector("h2.jobTitle")
                company = card.query_selector("[data-testid='company-name']")
                location_el = card.query_selector("[data-testid='text-location']")
                link_el = card.query_selector("h2.jobTitle a")
                
                jobs.append({
                    "titre": title.inner_text().strip() if title else "N/A",
                    "entreprise": company.inner_text().strip() if company else "N/A",
                    "lieu": location_el.inner_text().strip() if location_el else "N/A",
                    "lien": "https://be.indeed.com" + link_el.get_attribute("href") if link_el else "N/A",
                    "query": query,
                    "location": location,
                })
            except Exception as e:
                print(f"  Erreur sur une carte : {e}")
                continue
        
        browser.close()
    
    return jobs


if __name__ == "__main__":
    results = scrape_indeed("data analyst", "Bruxelles", max_jobs=5)
    for job in results:
        print(job)
        