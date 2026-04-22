import time
import json
import sys
from playwright.sync_api import sync_playwright


def scrape_indeed(query: str, location: str, max_jobs: int = 20) -> list[dict]:
    url = f"https://be.indeed.com/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}&lang=fr"
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({
            "Accept-Language": "fr-BE,fr;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(2)
        cards = page.query_selector_all("div.job_seen_beacon")

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
            except:
                continue
        browser.close()
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