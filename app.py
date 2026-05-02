import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Nassau Candy Distributor Dashboard")

# Load data
df = pd.read_csv("Nassau Candy Distributor.csv")

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

# Lead time
df["Lead_Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
df = df[df["Lead_Time"] >= 0]

st.header("Data Overview")
st.dataframe(df.head())

st.header("Lead Time by Region")
fig, ax = plt.subplots()
sns.barplot(x="Region", y="Lead_Time", data=df, ax=ax)
st.pyplot(fig)

# Add more visualizations as needed