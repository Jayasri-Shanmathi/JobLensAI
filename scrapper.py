# scraper.py
import requests
import pandas as pd

def scrape_jobs():
    url = "https://remotive.com/api/remote-jobs"
    response = requests.get(url)

    if response.status_code == 200:
        jobs_data = response.json().get("jobs", [])

        jobs = []
        for job in jobs_data[:50]:  # limit to 50 jobs for now
            jobs.append({
                "title": job.get("title", ""),
                "company": job.get("company_name", ""),
                "location": job.get("candidate_required_location", ""),
                "stack": job.get("job_type", ""),
            })

        df = pd.DataFrame(jobs)
        df.to_csv("jobs.csv", index=False)
        print(f"✅ Scraped {len(df)} jobs and saved to jobs.csv")
    else:
        print("⚠️ Failed to fetch jobs:", response.status_code)

if __name__ == "__main__":
    scrape_jobs()
