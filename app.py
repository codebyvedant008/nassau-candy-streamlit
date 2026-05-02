import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Nassau Candy Optimizer",
    page_icon="🏭",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("Nassau Candy Distributor.csv")

# Convert Dates
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

# Create Lead Time
df["Lead_Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
df = df[df["Lead_Time"] >= 0]

# =========================
# HEADER
# =========================
st.title("🏭 Nassau Candy Optimization Dashboard")
st.caption("AI-powered factory allocation & shipping intelligence")

st.markdown("---")

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + list(df["Region"].dropna().unique())
)

product = st.sidebar.selectbox(
    "Select Product",
    ["All"] + list(df["Product Name"].dropna().unique())
)

ship_mode = st.sidebar.selectbox(
    "Select Ship Mode",
    ["All"] + list(df["Ship Mode"].dropna().unique())
)

# Apply Filters
filtered = df.copy()

if region != "All":
    filtered = filtered[filtered["Region"] == region]

if product != "All":
    filtered = filtered[filtered["Product Name"] == product]

if ship_mode != "All":
    filtered = filtered[filtered["Ship Mode"] == ship_mode]

# =========================
# KPI CARDS
# =========================
col1,col2,col3,col4 = st.columns(4)
col1.metric("Orders", len(df))
col2.metric("Avg Lead Time", round(df["Lead_Time"].mean(),1))
col3.metric("Sales", f"${df['Sales'].sum():,.0f}")
col4.metric("Profit", f"${df['Gross Profit'].sum():,.0f}")

st.markdown("---")

# =========================
# CHARTS ROW 1
# =========================
col5, col6 = st.columns(2)

with col5:
    st.subheader("📍 Lead Time by Region")
    chart1 = filtered.groupby("Region")["Lead_Time"].mean()
    st.bar_chart(chart1)

with col6:
    st.subheader("🚚 Sales by Ship Mode")
    chart2 = filtered.groupby("Ship Mode")["Sales"].sum()
    st.bar_chart(chart2)

# =========================
# TOP PRODUCTS
# =========================
st.subheader("🍫 Top 10 Products by Sales")

top_products = (
    filtered.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)

# =========================
# RECOMMENDATION ENGINE
# =========================
st.subheader("🤖 Smart Recommendation")

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
    f"Recommend reallocating '{top_product}' to a nearer factory "
    f"to improve shipping speed and efficiency."
)

# =========================
# DATA TABLE
# =========================
st.subheader("📄 Data Preview")
st.dataframe(filtered.head(20))

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Built by Vedant | Data Analyst Internship Project")
