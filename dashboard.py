import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt

# ---------------------------
# Load CSV robustly
# ---------------------------
try:
    df = pd.read_csv("jobs.csv")
except FileNotFoundError:
    st.error("Error: jobs.csv not found.")
    df = pd.DataFrame()

df.columns = df.columns.str.strip()

# ---------------------------
# Streamlit App UI
# ---------------------------
st.title("JobLensAI Dashboard")

job_filter = st.text_input("Filter jobs (leave empty for all):")

if job_filter:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(job_filter, case=False).any(), axis=1)]
else:
    filtered_df = df.copy()

st.write(f"Total jobs found: {len(filtered_df)}")

# ---------------------------
# Count skills in job titles
# ---------------------------
skills = ["python", "java", "sql", "react", "django", "c#", "ai", "data"]

skill_counts = {
    skill: int(filtered_df["title"].str.lower().str.contains(skill).sum())
    for skill in skills
}

# Convert to DataFrame for plotting
skill_df = pd.DataFrame(list(skill_counts.items()), columns=["Skill", "Count"])
skill_df = skill_df[skill_df["Count"] > 0]  # show only non-zero

if not skill_df.empty:
    # ---------------------------
    # Bar chart of skill counts
    # ---------------------------
    st.subheader("Skill Occurrences (Bar Chart)")
    chart = alt.Chart(skill_df).mark_bar().encode(
        x=alt.X("Skill", sort='-y'),
        y="Count",
        tooltip=["Skill", "Count"]
    )
    st.altair_chart(chart, use_container_width=True)

    # ---------------------------
    # Pie chart of skill distribution
    # ---------------------------
    st.subheader("Skill Distribution (Pie Chart)")
    fig, ax = plt.subplots()
    ax.pie(
        skill_df["Count"],
        labels=skill_df["Skill"],
        autopct='%1.1f%%',
        startangle=90
    )
    ax.axis("equal")  # Equal aspect ratio → perfect circle
    st.pyplot(fig)
else:
    st.info("No skills found in job titles for the current filter.")

# ---------------------------
# Show job listings
# ---------------------------
st.subheader("Job Listings")
st.dataframe(filtered_df)
