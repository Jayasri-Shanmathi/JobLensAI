# scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_indeed_jobs(query="data scientist", location="India", pages=1):
    jobs = []
    base_url = "https://www.indeed.com/jobs"

    for page in range(0, pages*10, 10):
        params = {"q": query, "l": location, "start": page}
        response = requests.get(base_url, params=params, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        for job_card in soup.select(".job_seen_beacon"):
            title = job_card.select_one("h2 span")
            company = job_card.select_one(".companyName")
            loc = job_card.select_one(".companyLocation")
            summary = job_card.select_one(".job-snippet")

            jobs.append({
                "title": title.text.strip() if title else None,
                "company": company.text.strip() if company else None,
                "location": loc.text.strip() if loc else None,
                "summary": summary.text.strip() if summary else None
            })

    return pd.DataFrame(jobs)

if __name__ == "__main__":
    df = scrape_indeed_jobs(query="python developer", location="India", pages=2)
    df.to_csv("jobs.csv", index=False)
    print("✅ Scraped and saved jobs.csv with", len(df), "rows")
