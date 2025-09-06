import os
import pandas as pd
import streamlit as st
import scraper  # make sure scraper.py is in the same folder

st.set_page_config(page_title="JobLens AI", layout="wide")

def load_data():
    # If jobs.csv doesn't exist or is empty, trigger scraper
    if not os.path.exists("jobs.csv") or os.path.getsize("jobs.csv") == 0:
        st.info("📡 Fetching latest job postings...")
        scraper.scrape_jobs()

    # Try loading again
    if os.path.exists("jobs.csv") and os.path.getsize("jobs.csv") > 0:
        return pd.read_csv("jobs.csv")
    else:
        st.warning("⚠️ No job data available. Please try again later.")
        return pd.DataFrame(columns=["title", "company", "location", "stack"])

# Load data
df = load_data()

st.title("💼 JobLens AI - Job Trends Dashboard")

if not df.empty:
    # Sidebar filters
    st.sidebar.header("🔎 Filters")
    locations = st.sidebar.multiselect("Filter by Location", options=df["location"].unique())
    stacks = st.sidebar.multiselect("Filter by Stack", options=df["stack"].unique())

    filtered_df = df.copy()
    if locations:
        filtered_df = filtered_df[filtered_df["location"].isin(locations)]
    if stacks:
        filtered_df = filtered_df[filtered_df["stack"].isin(stacks)]

    st.write(f"### Showing {len(filtered_df)} job postings")
    st.dataframe(filtered_df)

    # Job counts by location
    st.subheader("📍 Job Distribution by Location")
    st.bar_chart(filtered_df["location"].value_counts())

    # Job counts by stack
    st.subheader("🛠️ Job Distribution by Tech Stack")
    st.bar_chart(filtered_df["stack"].value_counts())
else:
    st.error("No job postings found. Please try again later.")
