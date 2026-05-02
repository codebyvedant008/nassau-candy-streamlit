import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Nassau Candy AI Optimizer",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS (ULTRA PREMIUM DARK THEME)
# ==================================================
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main {
    background-color: #0e1117;
}
h1, h2, h3, h4, h5 {
    color: white;
}
div[data-testid="metric-container"] {
    background: linear-gradient(135deg,#1f2937,#111827);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #2d3748;
    box-shadow: 0 0 15px rgba(0,255,255,0.08);
}
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}
.stTabs [data-baseweb="tab"] {
    background-color:#1f2937;
    padding:10px 18px;
    border-radius:10px;
}
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================
df = pd.read_csv("Nassau Candy Distributor.csv")

# Date conversion
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

# Lead Time
df["Lead_Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
df = df[df["Lead_Time"] >= 0]

# ==================================================
# HEADER
# ==================================================
st.markdown("""
# 🏭 Nassau Candy AI Factory Optimizer
### Premium Logistics Intelligence Dashboard
""")

st.markdown("---")

# ==================================================
# SIDEBAR FILTERS
# ==================================================
st.sidebar.title("⚙ Control Panel")

region = st.sidebar.selectbox(
    "🌍 Select Region",
    ["All"] + sorted(df["Region"].dropna().unique())
)

product = st.sidebar.selectbox(
    "🍫 Select Product",
    ["All"] + sorted(df["Product Name"].dropna().unique())
)

ship = st.sidebar.selectbox(
    "🚚 Ship Mode",
    ["All"] + sorted(df["Ship Mode"].dropna().unique())
)

# Apply filters
filtered = df.copy()

if region != "All":
    filtered = filtered[filtered["Region"] == region]

if product != "All":
    filtered = filtered[filtered["Product Name"] == product]

if ship != "All":
    filtered = filtered[filtered["Ship Mode"] == ship]

# ==================================================
# KPI CARDS
# ==================================================
col1,col2,col3,col4 = st.columns(4)

col1.metric("📦 Orders", len(filtered))
col2.metric("⏱ Avg Lead Time", round(filtered["Lead_Time"].mean(),1))
col3.metric("💰 Sales", f"${filtered['Sales'].sum():,.0f}")
col4.metric("📈 Profit", f"${filtered['Gross Profit'].sum():,.0f}")

st.markdown("---")

# ==================================================
# TABS
# ==================================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Dashboard", "🤖 AI Insights", "📄 Data Center", "👤 About"]
)

# ==================================================
# DASHBOARD TAB
# ==================================================
with tab1:

    c1,c2 = st.columns(2)

    with c1:
        reg = filtered.groupby("Region")["Lead_Time"].mean().reset_index()
        fig1 = px.bar(
            reg,
            x="Region",
            y="Lead_Time",
            title="Lead Time by Region",
            template="plotly_dark"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        shipm = filtered.groupby("Ship Mode")["Sales"].sum().reset_index()
        fig2 = px.pie(
            shipm,
            names="Ship Mode",
            values="Sales",
            title="Sales Share by Ship Mode",
            template="plotly_dark"
        )
        st.plotly_chart(fig2, use_container_width=True)

    top = (
        filtered.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig3 = px.bar(
        top,
        x="Product Name",
        y="Sales",
        title="Top 10 Products by Sales",
        template="plotly_dark"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ==================================================
# AI INSIGHTS TAB
# ==================================================
with tab2:

    st.subheader("🤖 Smart Recommendation Engine")

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
        f"✔ Region needing urgent optimization: {slow_region}"
    )

    st.info(
        f"📌 Recommended product for factory reassignment: {top_product}"
    )

    st.warning(
        "⚠ Current delays may impact customer satisfaction and margins."
    )

# ==================================================
# DATA TAB
# ==================================================
with tab3:

    st.subheader("📄 Live Data Center")
    st.dataframe(filtered, use_container_width=True)

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV Report",
        csv,
        "Nassau_Report.csv",
        "text/csv"
    )

# ==================================================
# ABOUT TAB
# ==================================================
with tab4:

    st.markdown("""
# 👨‍💻 About Developer

## Vedant Vinay Pal  
### Data Analyst Intern | AI & Business Intelligence Enthusiast

---

## 📌 Project Overview

Factory Reallocation & Shipping Optimization Recommendation System developed for **Nassau Candy Distributor** to improve delivery speed, reduce logistics inefficiencies, and maximize profitability using Machine Learning & Data Analytics.

---

## 🚀 Key Features

✅ Predict Shipping Lead Time  
✅ Smart Factory Reallocation Suggestions  
✅ Profit & Efficiency Optimization  
✅ Interactive Visual Dashboard  
✅ Downloadable Reports

---

## 🛠 Technologies Used

**Python | Pandas | Streamlit | Plotly | Scikit-learn | Machine Learning**

---

## 🔗 Project Resources

### 📂 GitHub Repository  
https://github.com/codebyvedant008/nassau-candy-streamlit

### 📄 Research Paper PDF  
https://drive.google.com/file/d/1_0YIeYSgzncOJQ0AcfvLbW9dWs-L3NpQ/view?usp=drive_link

### 🌐 Live Streamlit Dashboard  
https://ann8rthzc5gfnvps6w8avu.streamlit.app/

---

## 📈 Career Objective

Passionate about solving real-world business problems through data, dashboards, and intelligent systems.

""")

    st.success("🚀 Thank you for visiting this premium analytics project!")
