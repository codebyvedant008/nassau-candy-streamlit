import pandas as pd

df = pd.read_csv("Nassau Candy Distributor.csv")

print("Dataset Loaded Successfully!")
print("Rows, Columns:", df.shape)
print(df.head())