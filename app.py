import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Read processed data
df = pd.read_csv("processed_data.csv")

# Handle column names
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

app = Dash(__name__)

app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f4f7fb",
        "padding": "30px",
        "minHeight": "100vh"
    },
    children=[
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "25px",
                "borderRadius": "15px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.1)",
                "maxWidth": "1200px",
                "margin": "auto"
            },
            children=[
                html.H1(
                    "Pink Morsel Sales Visualiser",
                    style={
                        "textAlign": "center",
                        "color": "#263859",
                        "fontSize": "36px",
                        "marginBottom": "10px"
                    }
                ),

                html.P(
                    "Explore Pink Morsel sales before and after the price increase on 15 January 2021.",
                    style={
                        "textAlign": "center",
                        "color": "#555",
                        "fontSize": "17px",
                        "marginBottom": "30px"
                    }
                ),

                html.Div(
                    style={
                        "backgroundColor": "#eef3ff",
                        "padding": "18px",
                        "borderRadius": "12px",
                        "marginBottom": "25px",
                        "textAlign": "center"
                    },
                    children=[
                        html.H3(
                            "Filter Sales by Region",
                            style={
                                "color": "#263859",
                                "marginBottom": "15px"
                            }
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
                            style={
                                "fontSize": "16px",
                                "color": "#333"
                            },
                            inputStyle={
                                "marginRight": "6px",
                                "marginLeft": "18px"
                            }
                        )
                    ]
                ),

                dcc.Graph(
                    id="sales-line-chart",
                    style={
                        "borderRadius": "12px",
                        "overflow": "hidden"
                    }
                )
            ]
        )
    ]
)


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df.copy()
        chart_title = "Pink Morsel Sales Across All Regions"
    else:
        filtered_df = df[df[region_column].str.lower() == selected_region].copy()
        chart_title = f"Pink Morsel Sales in {selected_region.title()} Region"

    daily_sales = filtered_df.groupby(date_column, as_index=False)[sales_column].sum()

    fig = px.line(
        daily_sales,
        x=date_column,
        y=sales_column,
        title=chart_title,
        labels={
            date_column: "Date",
            sales_column: "Sales"
        }
    )

    fig.add_vline(
        x="2021-01-15",
        line_dash="dash",
        annotation_text="Price Increase - 15 Jan 2021",
        annotation_position="top left"
    )

    fig.update_layout(
        plot_bgcolor="#f8fbff",
        paper_bgcolor="#ffffff",
        title={
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 22}
        },
        xaxis_title="Date",
        yaxis_title="Sales",
        font={"family": "Arial", "size": 14, "color": "#263859"},
        margin={"l": 50, "r": 30, "t": 70, "b": 50}
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)