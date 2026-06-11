import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Read processed data from Task 2
df = pd.read_csv("processed_data.csv")

# Convert Date column safely
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])
    date_column = "Date"
    sales_column = "Sales"
    region_column = "Region"
else:
    df["date"] = pd.to_datetime(df["date"])
    date_column = "date"
    sales_column = "sales"
    region_column = "region"

# Sort data by date
df = df.sort_values(by=date_column)

# Group sales by date
daily_sales = df.groupby(date_column, as_index=False)[sales_column].sum()

# Create line chart
fig = px.line(
    daily_sales,
    x=date_column,
    y=sales_column,
    title="Pink Morsel Sales Before and After Price Increase",
    labels={
        date_column: "Date",
        sales_column: "Sales"
    }
)

# Add price increase reference line
fig.add_vline(
    x="2021-01-15",
    line_dash="dash",
    annotation_text="Price Increase - 15 Jan 2021",
    annotation_position="top left"
)

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        "Pink Morsel Sales Visualiser",
        style={"textAlign": "center"}
    ),

    html.P(
        "This dashboard shows Pink Morsel sales before and after the price increase on 15 January 2021.",
        style={"textAlign": "center"}
    ),

    dcc.Graph(
        id="pink-morsel-sales-line-chart",
        figure=fig
    )
])

if __name__ == "__main__":
    app.run(debug=True)