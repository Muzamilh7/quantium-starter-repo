import pandas as pd
import glob

files = glob.glob("data/*.csv")

df_list = []

for file in files:
    df = pd.read_csv(file)

    # keep only pink morsels
    df = df[df["product"] == "pink morsel"]

    # clean quantity and price
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = df["price"].replace("[$,]", "", regex=True)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # create sales
    df["sales"] = df["quantity"] * df["price"]

    # keep required columns
    df = df[["sales", "date", "region"]]

    df_list.append(df)

final_df = pd.concat(df_list)
final_df.to_csv("output.csv", index=False)

print("Task 2 complete")