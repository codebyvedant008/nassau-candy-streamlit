import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_csv("Nassau Candy Distributor.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

df["Lead_Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
df = df[df["Lead_Time"] >= 0]

df["Month"] = df["Order Date"].dt.month
df["Year"] = df["Order Date"].dt.year
df["Profit_Margin"] = df["Gross Profit"] / df["Sales"]

X = df[[
    "Region","Ship Mode","Product Name","Division",
    "Sales","Units","Cost","Month","Year","Profit_Margin"
]]

y = df["Lead_Time"]

cat_cols = ["Region","Ship Mode","Product Name","Division"]
num_cols = ["Sales","Units","Cost","Month","Year","Profit_Margin"]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

prep = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ("num", "passthrough", num_cols)
])

model = Pipeline([
    ("prep", prep),
    ("gb", GradientBoostingRegressor())
])

model.fit(X_train,y_train)

pred = model.predict(X_test)

print("Improved Model")
print("MAE:", round(mean_absolute_error(y_test,pred),2))
print("R2:", round(r2_score(y_test,pred),2))