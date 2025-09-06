# scraper.py
import requests
import pandas as pd

def scrape_jobs():
    url = "https://remotive.com/api/remote-jobs"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            jobs_data = response.json().get("jobs", [])

            if jobs_data:  # ✅ only save if jobs found
                jobs = []
                for job in jobs_data[:50]:
                    jobs.append({
                        "title": job.get("title", ""),
                        "company": job.get("company_name", ""),
                        "location": job.get("candidate_required_location", ""),
                        "stack": job.get("job_type", ""),
                    })

                df = pd.DataFrame(jobs)
                df.to_csv("jobs.csv", index=False)
                print(f"✅ Scraped {len(df)} jobs and saved to jobs.csv")
                return
    except Exception as e:
        print("⚠️ Error while scraping:", e)

    # Fallback → write dummy data if API fails or empty
    print("⚠️ No jobs found, using dummy data instead")
    jobs = [
        {"title": "Data Scientist", "company": "TechCorp", "location": "Bangalore", "stack": "Python"},
        {"title": "AI Engineer", "company": "InnovateAI", "location": "Chennai", "stack": "TensorFlow"},
        {"title": "Backend Developer", "company": "CloudNet", "location": "Hyderabad", "stack": "Java"},
        {"title": "Frontend Developer", "company": "Webify", "location": "Remote", "stack": "React"},
    ]
    df = pd.DataFrame(jobs)
    df.to_csv("jobs.csv", index=False)
    print("✅ Saved dummy jobs.csv with", len(df), "rows")

if __name__ == "__main__":
    scrape_jobs()
