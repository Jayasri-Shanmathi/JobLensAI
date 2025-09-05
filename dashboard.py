# dashboard.py
import streamlit as st
import pandas as pd
import altair as alt

st.title("📊 JobLensAI - Job Trends Dashboard")

df = pd.read_csv("jobs.csv")

# Sidebar filters
location_filter = st.sidebar.selectbox("Filter by Location", ["All"] + df["location"].dropna().unique().tolist())

filtered_df = df if location_filter == "All" else df[df["location"] == location_filter]

st.subheader("Job Listings")
st.dataframe(filtered_df)

# Skill Analysis
skills = ["python", "java", "react", "aws", "sql"]
skill_counts = {skill: filtered_df["summary"].str.lower().str.contains(skill).sum() for skill in skills}
skill_df = pd.DataFrame(list(skill_counts.items()), columns=["Skill", "Count"])

chart = alt.Chart(skill_df).mark_bar().encode(
    x="Skill",
    y="Count",
    tooltip=["Skill", "Count"]
)

st.subheader("Skill Demand")
st.altair_chart(chart, use_container_width=True)
