import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("Nassau Candy Distributor.csv")

# Product-Factory Mapping
factory_map = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory"
}

all_factories = [
    "Lot's O' Nuts",
    "Wicked Choccy's",
    "Sugar Shack",
    "Secret Factory",
    "The Other Factory"
]

# Assign current factory
df["Current_Factory"] = df["Product Name"].map(factory_map)

# Average lead time per product
summary = df.groupby("Product Name").agg({
    "Sales":"sum",
    "Gross Profit":"sum",
    "Units":"sum"
}).reset_index()

recommendations = []

for _, row in summary.iterrows():

    product = row["Product Name"]
    current = factory_map.get(product, "Unknown")

    # Simulated current score
    current_score = np.random.randint(60, 80)

    best_factory = current
    best_score = current_score

    for fac in all_factories:
        if fac != current:
            score = np.random.randint(65, 95)

            if score > best_score:
                best_score = score
                best_factory = fac

    improvement = best_score - current_score

    recommendations.append([
        product,
        current,
        best_factory,
        improvement
    ])

rec_df = pd.DataFrame(recommendations,
columns=[
    "Product Name",
    "Current Factory",
    "Recommended Factory",
    "Improvement Score"
])

rec_df = rec_df.sort_values(
    by="Improvement Score",
    ascending=False
)

print(rec_df)