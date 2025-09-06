import os
import pandas as pd
import streamlit as st
import scraper  # make sure scraper.py exists

st.set_page_config(page_title="JobLens AI", layout="wide")

# Safe loader
def load_data(force_refresh=False):
    if force_refresh or not os.path.exists("jobs.csv") or os.path.getsize("jobs.csv") == 0:
        st.info("📡 Fetching latest job postings...")
        try:
            scraper.scrape_jobs()
        except Exception as e:
            st.error(f"❌ Error while scraping: {e}")

    if os.path.exists("jobs.csv") and os.path.getsize("jobs.csv") > 0:
        try:
            return pd.read_csv("jobs.csv")
        except pd.errors.EmptyDataError:
            st.error("⚠️ jobs.csv is empty or corrupted.")
            return pd.DataFrame(columns=["title", "company", "location", "stack"])
    else:
        return pd.DataFrame(columns=["title", "company", "location", "stack"])

# Sidebar
st.sidebar.header("⚙️ Controls")
refresh = st.sidebar.button("🔄 Refresh Jobs")

# Load data safely
df = load_data(force_refresh=refresh)

# Title
st.title("💼 JobLens AI - Job Trends Dashboard")

if not df.empty:
    # Filters
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

    # Charts
    st.subheader("📍 Job Distribution by Location")
    if not filtered_df["location"].empty:
        st.bar_chart(filtered_df["location"].value_counts())

    st.subheader("🛠️ Job Distribution by Tech Stack")
    if not filtered_df["stack"].empty:
        st.bar_chart(filtered_df["stack"].value_counts())
else:
    st.warning("⚠️ No job postings available. Click 'Refresh Jobs' to fetch.")
