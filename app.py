import streamlit as st
import pandas as pd
import numpy as np

# Page setup
st.set_page_config(
    page_title="Nassau Candy Optimizer",
    page_icon="🏭",
    layout="wide"
)

# Load Data
df = pd.read_csv("Nassau Candy Distributor.csv")

# Dates
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

# Lead Time
df["Lead_Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
df = df[df["Lead_Time"] >= 0]

# =======================
# HEADER
# =======================
st.title("🏭 Nassau Candy Factory Optimization Dashboard")
st.markdown("### AI-Powered Shipping & Factory Recommendation System")

# =======================
# SIDEBAR
# =======================
st.sidebar.header("🔍 Filters")

region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + list(df["Region"].dropna().unique())
)

product = st.sidebar.selectbox(
    "Select Product",
    ["All"] + list(df["Product Name"].dropna().unique())
)

shipmode = st.sidebar.selectbox(
    "Select Ship Mode",
    ["All"] + list(df["Ship Mode"].dropna().unique())
)

# Apply filters
filtered = df.copy()

if region != "All":
    filtered = filtered[filtered["Region"] == region]

if product != "All":
    filtered = filtered[filtered["Product Name"] == product]

if shipmode != "All":
    filtered = filtered[filtered["Ship Mode"] == shipmode]

# =======================
# KPI CARDS
# =======================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", len(filtered))
col2.metric("Avg Lead Time", round(filtered["Lead_Time"].mean(), 1))
col3.metric("Total Sales", f"${filtered['Sales'].sum():,.0f}")
col4.metric("Total Profit", f"${filtered['Gross Profit'].sum():,.0f}")

st.markdown("---")

# =======================
# CHARTS
# =======================
col5, col6 = st.columns(2)

with col5:
    st.subheader("📈 Lead Time by Region")
    region_chart = filtered.groupby("Region")["Lead_Time"].mean()
    st.bar_chart(region_chart)

with col6:
    st.subheader("💰 Sales by Ship Mode")
    sales_chart = filtered.groupby("Ship Mode")["Sales"].sum()
    st.bar_chart(sales_chart)

# =======================
# PRODUCT ANALYSIS
# =======================
st.subheader("🍫 Top Products by Sales")

top_products = (
    filtered.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)

# =======================
# RECOMMENDATION ENGINE
# =======================
st.subheader("🤖 Recommendation Insights")

slow_region = (
    filtered.groupby("Region")["Lead_Time"]
    .mean()
    .sort_values(ascending=False)
    .index[0]
)

top_product = (
    filtered.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

st.success(
    f"⚡ {slow_region} region has the highest lead time. "
    f"Consider reallocating high-demand product '{top_product}' "
    f"to a nearer factory for faster delivery."
)

# =======================
# DATA TABLE
# =======================
st.subheader("📄 Raw Data Preview")
st.dataframe(filtered.head(20))

# =======================
# FOOTER
# =======================
st.markdown("---")
st.caption("Built by Vedant | Data Analyst Internship Project 🚀")
