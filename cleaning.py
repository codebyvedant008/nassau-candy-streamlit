import pandas as pd

# Load dataset
df = pd.read_csv("Nassau Candy Distributor.csv")

# Show columns
print("Columns in dataset:")
print(df.columns)

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

# Create Lead Time
df["Lead_Time"] = (df["Ship Date"] - df["Order Date"]).dt.days

# Check null values
print("\nNull Values:")
print(df.isnull().sum())

# Basic info
print("\nDataset Shape:", df.shape)

# Lead time summary
print("\nLead Time Summary:")
print(df["Lead_Time"].describe())

# First rows
print("\nPreview:")
print(df.head())