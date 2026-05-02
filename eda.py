import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("Nassau Candy Distributor.csv")

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

# Lead time
df["Lead_Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
df = df[df["Lead_Time"] >= 0]

sns.set_style("whitegrid")

# 1. Lead Time by Region
plt.figure(figsize=(10,5))
sns.barplot(x="Region", y="Lead_Time", data=df)
plt.title("Average Lead Time by Region")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Profit by Ship Mode
plt.figure(figsize=(8,5))
sns.barplot(x="Ship Mode", y="Gross Profit", data=df)
plt.title("Gross Profit by Ship Mode")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# 3. Top 10 Products by Sales
top_products = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
top_products.plot(kind="bar")
plt.title("Top 10 Products by Sales")
plt.tight_layout()
plt.show()

# 4. Correlation Heatmap
plt.figure(figsize=(8,5))
sns.heatmap(df[["Sales","Units","Gross Profit","Cost","Lead_Time"]].corr(),
            annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()