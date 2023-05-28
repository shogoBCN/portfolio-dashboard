import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

import pandas as pd

pd.options.mode.chained_assignment = None

import plotly.graph_objects as go
import plotly.express.colors as colors
import plotly.express as px
from plotly.subplots import make_subplots

import dash
from dash import dcc, dash_table, html, Output, Input

from variables import (
    df_bob,
    products,
    prod_sales_12,
    prod_sales_6,
    prod_sales_3,
    region_dict,
    asr,
    gdf_fig,
    apr,
    kpi_one_fig,
    KPI_Two_fig,
)
from bs_comps import button_group, time_radios


app = dash.Dash(
    __name__, suppress_callback_exceptions=True, title="EasyMoney Dashboard"
)
server = app.server

app.layout = html.Div(
    [
        html.Div(
            className="main_Frame",
            children=[
                html.Div(
                    className="header_div",
                    children=[
                        html.Img(
                            className="_logo",
                            src=app.get_asset_url("../assets/easymoney.png"),
                        ),
                        html.H1("Data Dashboard", className="page_Title"),
                        html.H1("     ", className="dummy"),
                    ],
                ),
                dcc.Tabs(
                    id="tab_frame",
                    value="regions",
                    className="custom-tabs-container",
                    parent_className="custom-tabs",
                    children=[
                        dcc.Tab(
                            label="Regions",
                            value="regions",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            label="Products",
                            value="products",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            label="KPIs",
                            value="kpis",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                    ],
                ),
                html.Div(id="tabs_content"),
            ],
        )
    ]
)


@app.callback(Output("tabs_content", "children"), Input("tab_frame", "value"))
def render_content(tab):
    if tab == "regions":
        return html.Div(
            className="content_frame parent-container",
            children=[
                html.Div(className="Spacer"),
                dcc.Dropdown(
                    className="product_dropdown",
                    id="region_dropdown",
                    options=region_dict,
                    value="Barcelona",
                    style={"width": "50%", "margin": "0 auto"},
                ),
                html.Div(className="Spacer"),
                html.Div(
                    className="content_row parent-container",
                    children=[
                        html.Div(
                            className="card_frame graph_frame",
                            children=[
                                html.Div(
                                    className="ef",
                                    children=[
                                        dcc.Graph(id="region_map", figure=gdf_fig)
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className="content_row parent-container centered_element",
                            children=[
                                html.Div(
                                    className="content-container_regions ",
                                    children=[
                                        html.Div(className="Spacer"),
                                        html.Label(
                                            className="feedback_number_label",
                                            children=[
                                                "Σ Users",
                                                html.Div(
                                                    className="feedback_number_frame",
                                                    children=[
                                                        html.Span(id="users_number")
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Div(className="Spacer_12"),
                                        html.Label(
                                            className="feedback_number_label",
                                            children=[
                                                "Σ Product Sales",
                                                html.Div(
                                                    className="feedback_number_frame",
                                                    children=[
                                                        html.Span(id="sales_number")
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="content-container_regions",
                                    children=[
                                        html.Div(className="Spacer"),
                                        html.Label(
                                            className="feedback_number_label",
                                            children=[
                                                "Ø Age",
                                                html.Div(
                                                    className="feedback_number_frame",
                                                    children=[
                                                        html.Span(id="age_number")
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Div(className="Spacer_12"),
                                        html.Label(
                                            className="feedback_number_label",
                                            children=[
                                                "Ø Retention",
                                                html.Div(
                                                    className="feedback_number_frame",
                                                    children=[
                                                        html.Span(id="reten_number")
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(className="Spacer"),
                html.Div(
                    className="parent-container",
                    children=[
                        html.Div(className="Spacer_12"),
                        html.Div(
                            className="content-container_regions",
                            children=[
                                html.Div(
                                    className="card_frame",
                                    style={"margin-right": "10px"},
                                    children=[dcc.Graph(id="region_total_sold_graph")],
                                )
                            ],
                        ),
                        html.Div(
                            className="content-container_regions",
                            children=[
                                html.Div(
                                    className="card_frame",
                                    style={"margin-right": "10px"},
                                    children=[dcc.Graph(id="region_time_series")],
                                )
                            ],
                        ),
                    ],
                ),
            ],
        )

    if tab == "products":
        return html.Div(
            className="content_frame parent-container",
            children=[
                html.Div(className="Spacer"),
                # html.Div(
                # className = "centered_element",
                # children = [
                #    html.Div(
                #    className = "horizontal_control",
                #    children = [html.Div(button_group)])]),
                html.Div(
                    className="horizontal_control parent-container",
                    children=[html.Div(time_radios)],
                ),
                html.Div(
                    className="content_row parent-container",
                    children=[
                        html.Div(
                            className="card_frame graph_frame",
                            children=[dcc.Graph(id="product_sales_graph")],
                        )
                    ],
                ),
                html.Div(className="Spacer"),
                html.Div(
                    className="parent-container",
                    children=[
                        html.Div(
                            dcc.Dropdown(
                                className="product_dropdown",
                                id="product_dropdown",
                                options=[{"label": p, "value": p} for p in products],
                                value="debit_card",
                                style={"width": "50%", "margin": "0 auto"},
                            )
                        ),
                        html.Div(className="Spacer_12"),
                        html.Div(
                            className="content-container_prods",
                            children=[
                                html.Div(
                                    className="card_frame",
                                    style={"margin-right": "10px"},
                                    children=[dcc.Graph(id="retention_graph")],
                                )
                            ],
                        ),
                        html.Div(
                            className="content-container_prods",
                            children=[
                                html.Div(
                                    className="card_frame",
                                    style={"margin-right": "10px"},
                                    children=[dcc.Graph(id="progression_graph")],
                                )
                            ],
                        ),
                    ],
                ),
            ],
        )

    if tab == "kpis":
        return html.Div(
            className="content_frame parent-container",
            children=[
                html.Div(className="Spacer"),
                html.Div(
                    className="parent-container",
                    children=[
                        html.Div(className="Spacer_12"),
                        html.Div(
                            className="content-container_prods",
                            children=[
                                html.Div(
                                    className="card_frame",
                                    style={"margin-right": "10px"},
                                    children=[
                                        dcc.Graph(id="KPI_one", figure=kpi_one_fig)
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className="content-container_prods",
                            children=[
                                html.Div(
                                    className="card_frame",
                                    style={"margin-right": "10px"},
                                    children=[
                                        dcc.Graph(id="KPI_two", figure=KPI_Two_fig)
                                    ],
                                )
                            ],
                        ),
                    ],
                ),
            ],
        )


#################################
## region
#################################
# top sellers per region
@app.callback(
    Output("region_total_sold_graph", "figure"), [Input("region_dropdown", "value")]
)
def plot_all_sales(region):
    data = (
        asr[asr["region"] == region]
        .groupby(["variable"])["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    trace = go.Bar(x=data.index, y=data.values)
    layout = go.Layout(
        title=dict(text=f"{region}: Top Sellers", x=0.5),
        yaxis=dict(title="Sales Count"),
        autosize=True,
        height=300,
        margin={"t": 32, "b": 10, "l": 2, "r": 2},
    )
    fig = go.Figure(data=[trace], layout=layout)
    fig.update_traces(marker=dict(color="MediumSeaGreen"))
    return fig


# over time total sales per region
@app.callback(
    Output("region_time_series", "figure"), [Input("region_dropdown", "value")]
)
def plot_all_sales(region):
    data = (
        df_bob[df_bob["region"] == region]
        .groupby(["pk_cid"])
        .agg({"age": "max", "active_customer": "max"})
    )
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=data[data["active_customer"] == 1]["age"],
            nbinsx=20,
            name="Active Customer",
            marker=dict(color="MediumSeaGreen"),
        )
    )
    fig.add_trace(
        go.Histogram(
            x=data[data["active_customer"] == 0]["age"],
            nbinsx=20,
            name="Inactive Customer",
            marker=dict(color="#ABEBC6"),
        )
    )
    fig.update_layout(
        title=dict(text="Age Distribution by Application Activity", x=0.5),
        yaxis=dict(title="User Count"),
        bargap=0.1,
        height=300,
        autosize=True,
        margin={"t": 67, "b": 10, "l": 2, "r": 2},
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


@app.callback(Output("users_number", "children"), [Input("region_dropdown", "value")])
def update_total_fb(region):
    return apr[apr["region"] == region]["pk_cid"].values[0]


@app.callback(Output("sales_number", "children"), [Input("region_dropdown", "value")])
def update_total_fb(region):
    return asr[asr["region"] == region].groupby(["pk_partition"])["sales"].sum().sum()


@app.callback(Output("age_number", "children"), [Input("region_dropdown", "value")])
def update_total_fb(region):
    return str(int(df_bob[df_bob["region"] == region]["age"].mean())) + " years"


@app.callback(Output("reten_number", "children"), [Input("region_dropdown", "value")])
def update_total_fb(region):
    temp = df_bob[(df_bob["region"] == region) & (df_bob["active_customer"] == 1)]
    product_tenure = []
    for product in products:
        test = temp.groupby(["pk_cid"])[product].sum()
        mean_tenure = test[test > 0].mean()
        product_tenure.append(mean_tenure)
    df_product_stats = pd.DataFrame(
        {"product": products, "mean_tenure": product_tenure}
    )
    return str(round(df_product_stats["mean_tenure"].mean(), 2)) + " months"


#################################
## products
#################################


# product sales count
@app.callback(
    Output("product_sales_graph", "figure"),
    [Input("user_type_buttons_2", "value")],  # Input("user_type_buttons", "value"),
)
def plot_all_sales(time_):
    if time_ == "1 year":
        data = prod_sales_12
    if time_ == "6 month":
        data = prod_sales_6
    if time_ == "3 month":
        data = prod_sales_3

    trace = go.Bar(x=data["Unnamed: 0"], y=data["All Users"], text=data["All Users"])
    layout = go.Layout(
        title=dict(text=f"Overall Product Activity Count", x=0.5),
        yaxis=dict(title="Product Activities"),
        autosize=True,
        height=225,
        margin={"t": 32, "b": 10, "l": 2, "r": 2},
    )
    fig = go.Figure(data=[trace], layout=layout)
    fig.update_traces(marker=dict(color="MediumSeaGreen"))
    return fig


# retention graph
@app.callback(Output("retention_graph", "figure"), [Input("product_dropdown", "value")])
def plot_product_retention(product):
    df_temp = df_bob.groupby("pk_partition")[product].sum().reset_index()
    trace = go.Scatter(x=df_temp["pk_partition"], y=df_temp[product], mode="lines")
    layout = go.Layout(
        title=dict(text="Accumulative Activity Count", x=0.5),
        yaxis=dict(title="Revenue Generating Activities"),
        autosize=True,
        height=225,
        margin={"t": 32, "b": 10, "l": 2, "r": 2},
    )
    fig = go.Figure(data=[trace], layout=layout)
    fig.update_traces(marker=dict(color="MediumSeaGreen"))
    return fig


# progression graph
@app.callback(
    Output("progression_graph", "figure"), [Input("product_dropdown", "value")]
)
def plot_product_progression(product):
    df_temp = df_bob.groupby("month_year").agg({product: "sum", "entry_date": "max"})
    df_temp["entry_date"] = pd.to_datetime(df_temp["entry_date"])
    df_temp = df_temp[df_temp["entry_date"] > "2018-01-01"]
    df_temp = df_temp.sort_values(by="entry_date", ascending=True)
    trace = go.Scatter(x=df_temp["entry_date"], y=df_temp[product], mode="lines")
    layout = go.Layout(
        title=dict(text="Monthly Product Engagement", x=0.5),
        yaxis=dict(title="Revenue Generating Activities"),
        autosize=True,
        height=225,
        margin={"t": 32, "b": 10, "l": 2, "r": 2},
    )
    fig = go.Figure(data=[trace], layout=layout)
    fig.update_traces(marker=dict(color="MediumSeaGreen"))
    return fig


#################################
if __name__ == "__main__":
    # app.run_server(debug = True, port = 8088)
    app.run_server(debug=False, host="0.0.0.0", port=80)
