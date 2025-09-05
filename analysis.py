# analysis.py
import pandas as pd
import matplotlib.pyplot as plt

# Load scraped data
df = pd.read_csv("jobs.csv")

# Drop missing values
df = df.dropna()

# Count jobs by location
job_location_count = df["location"].value_counts().head(10)

# Count jobs by keywords in summary
skills = ["python", "java", "react", "aws", "sql"]
skill_counts = {skill: df["summary"].str.lower().str.contains(skill).sum() for skill in skills}

print("Top Locations:\n", job_location_count)
print("\nSkill Demand:\n", skill_counts)

# Plot skill demand
plt.bar(skill_counts.keys(), skill_counts.values())
plt.title("Skill Demand in Job Postings")
plt.show()
