# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("Generated_Schedule.xlsx", engine="openpyxl")
    return df

df = load_data()

st.title("📘 Class Schedule Dashboard")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    instructor = st.selectbox("Instructor", ["All"] + sorted(df["Instructor"].unique().tolist()))
    section = st.selectbox("Section", ["All"] + sorted(df["Section"].unique().tolist()))
    day = st.selectbox("Day", ["All"] + sorted(df["Day"].unique().tolist()))

# Apply filters
filtered_df = df.copy()
if instructor != "All":
    filtered_df = filtered_df[filtered_df["Instructor"] == instructor]
if section != "All":
    filtered_df = filtered_df[filtered_df["Section"] == section]
if day != "All":
    filtered_df = filtered_df[filtered_df["Day"] == day]

# Show filtered table
st.subheader("📅 Schedule Table")
st.dataframe(filtered_df)

# Chart: Number of Classes per Instructor
st.subheader("👨‍🏫 Classes per Instructor")
instructor_counts = df["Instructor"].value_counts().reset_index()
instructor_counts.columns = ["Instructor", "Classes"]
fig = px.bar(instructor_counts, x="Instructor", y="Classes", title="Classes per Instructor")
st.plotly_chart(fig)

# Chart: Room Utilization
st.subheader("🏫 Room Utilization")
room_counts = df["Room"].value_counts().reset_index()
room_counts.columns = ["Room", "Classes"]
fig2 = px.bar(room_counts, x="Room", y="Classes", title="Room Usage")
st.plotly_chart(fig2)
