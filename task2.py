import pandas as pd
import glob

files = glob.glob("data/*.csv")

df_list = []

for file in files:
    df = pd.read_csv(file)

    df = df[df["product"] == "pink morsel"]
    df["sales"] = df["quantity"] * df["price"]
    df = df[["sales", "date", "region"]]

    df_list.append(df)

final_df = pd.concat(df_list)

final_df.to_csv("output.csv", index=False)

print("Task 2 complete")