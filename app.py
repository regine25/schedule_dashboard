import streamlit as st
import pandas as pd
from io import BytesIO
import os

# --- Set Page Configuration FIRST ---
st.set_page_config(page_title="School Schedule Dashboard", layout="wide")

# --- Check if Excel file exists ---
file_path = "Generated_Schedule.xlsx"
if not os.path.exists(file_path):
    st.error(f"❌ File not found: {file_path}")
    st.stop()  # Stop the app here if the file doesn't exist
else:
    st.success(f"✅ Excel file found: {file_path}")

# --- Load Excel File ---
@st.cache_data
def load_schedule():
    return pd.read_excel(file_path)

df = load_schedule()

st.title("📅 School Schedule Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Schedule")

instructors = st.sidebar.multiselect("Instructor", df["Instructor"].dropna().unique())
rooms = st.sidebar.multiselect("Room", df["Room"].dropna().unique())
sections = st.sidebar.multiselect("Section", df["Section"].dropna().unique())
days = st.sidebar.multiselect("Day", df["Day"].dropna().unique())

# --- Apply Filters ---
filtered_df = df.copy()

if instructors:
    filtered_df = filtered_df[filtered_df["Instructor"].isin(instructors)]
if rooms:
    filtered_df = filtered_df[filtered_df["Room"].isin(rooms)]
if sections:
    filtered_df = filtered_df[filtered_df["Section"].isin(sections)]
if days:
    filtered_df = filtered_df[filtered_df["Day"].isin(days)]

# --- Display Data ---
st.subheader("📋 Filtered Schedule")
st.dataframe(filtered_df, use_container_width=True)

# --- Download Filtered Schedule ---
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Schedule')
    return output.getvalue()

excel_data = to_excel(filtered_df)

st.download_button(
    label="📥 Download as Excel",
    data=excel_data,
    file_name="filtered_schedule.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
