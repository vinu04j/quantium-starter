import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_FILE = Path("processed_data.csv")

all_data = []

for file in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(file)
    all_data.append(df)

data = pd.concat(all_data, ignore_index=True)

data.columns = data.columns.str.strip().str.lower()

pink_morsel = data[data["product"].str.strip().str.lower() == "pink morsel"].copy()

pink_morsel["price"] = (
    pink_morsel["price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .astype(float)
)

pink_morsel["quantity"] = pink_morsel["quantity"].astype(int)

pink_morsel["sales"] = pink_morsel["price"] * pink_morsel["quantity"]

pink_morsel["date"] = pd.to_datetime(pink_morsel["date"])

processed_data = pink_morsel[["sales", "date", "region"]]

processed_data.to_csv(OUTPUT_FILE, index=False)

print("Processed data created successfully.")
print(processed_data.head())