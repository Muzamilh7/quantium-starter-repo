import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Load processed data
df = pd.read_csv("output.csv")
df["date"] = pd.to_datetime(df["date"])
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

app = Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": "#f4f6f8",
        "minHeight": "100vh",
        "padding": "30px",
        "fontFamily": "Arial, sans-serif",
    },
    children=[
        html.Div(
            style={
                "maxWidth": "1100px",
                "margin": "0 auto",
                "backgroundColor": "white",
                "padding": "30px",
                "borderRadius": "16px",
                "boxShadow": "0 4px 20px rgba(0,0,0,0.08)",
            },
            children=[
                html.H1(
                    "Soul Foods Pink Morsel Sales Visualiser",
                    style={
                        "textAlign": "center",
                        "marginBottom": "10px",
                        "color": "#222",
                    },
                ),

                html.P(
                    "Explore Pink Morsel sales over time and compare regions before and after the price increase.",
                    style={
                        "textAlign": "center",
                        "color": "#666",
                        "marginBottom": "30px",
                    },
                ),

                html.Label(
                    "Filter by Region:",
                    style={
                        "fontWeight": "bold",
                        "fontSize": "18px",
                        "display": "block",
                        "marginBottom": "12px",
                        "color": "#333",
                    },
                ),

                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    style={"marginBottom": "25px"},
                    labelStyle={
                        "marginRight": "20px",
                        "fontSize": "16px",
                        "color": "#444",
                    },
                ),

                dcc.Graph(id="sales-chart")
            ],
        )
    ],
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    filtered_df = df.copy()

    if selected_region != "all":
        filtered_df = filtered_df[filtered_df["region"].str.lower() == selected_region]

    sales_by_date = (
        filtered_df.groupby("date", as_index=False)["sales"]
        .sum()
        .sort_values("date")
    )

    fig = px.line(
        sales_by_date,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales Over Time - {selected_region.title()}",
        labels={"date": "Date", "sales": "Total Sales"},
    )

    fig.update_traces(mode="lines", line={"width": 3})

    fig.add_vline(
        x="2021-01-15",
        line_width=2,
        line_dash="dash",
        line_color="red"
    )

    fig.add_annotation(
        x="2021-01-15",
        y=sales_by_date["sales"].max() if not sales_by_date.empty else 0,
        text="Price Increase (15 Jan 2021)",
        showarrow=True,
        arrowhead=1
    )

    fig.update_layout(
        template="plotly_white",
        height=600,
        title_x=0.5,
        margin=dict(l=40, r=40, t=80, b=40)
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)