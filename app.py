import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Load the processed data
df = pd.read_csv("output.csv")

# Convert date column to datetime and sort
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Group sales by date
sales_by_date = df.groupby("date", as_index=False)["sales"].sum()

# Create line chart
fig = px.line(
    sales_by_date,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Sales"}
)

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Visualiser"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)