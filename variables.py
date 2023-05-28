import pandas as pd
import geopandas as gpd
import plotly.express.colors as colors
import plotly.express as px
import plotly.graph_objects as go
import os

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
FILES = "files"

#ALL_DF_PATH = os.path.join(CURRENT_PATH, FILES, "Bobs_dash_df.csv")
PRODUCT_SALES_12_PATH = os.path.join(CURRENT_PATH, FILES, "sales_12.csv")
PRODUCT_SALES_6_PATH = os.path.join(CURRENT_PATH, FILES, "sales_6.csv")
PRODUCT_SALES_3_PATH = os.path.join(CURRENT_PATH, FILES, "sales_3.csv")
SALES_REGION_PATH = os.path.join(CURRENT_PATH, FILES, "all_sales_region.csv")
ACTIVE_PER_REGION_PATH = os.path.join(CURRENT_PATH, FILES, "active_per_region.csv")
GDF_PATH = os.path.join(CURRENT_PATH, FILES, "Spain_regions.geojson")

apr = pd.read_csv(ACTIVE_PER_REGION_PATH)
gdf = gpd.read_file(GDF_PATH)
#df_bob = pd.read_csv(ALL_DF_PATH)
asr = pd.read_csv(SALES_REGION_PATH)
prod_sales_12 = pd.read_csv(PRODUCT_SALES_12_PATH)
prod_sales_6 = pd.read_csv(PRODUCT_SALES_6_PATH)
prod_sales_3 = pd.read_csv(PRODUCT_SALES_3_PATH)
df_bob = pd.read_csv("https://storage.googleapis.com/easymoneybobsdata/Bobs_dash_df.csv", 
                 dtype = {
                    "age": "uint8", 
                    "pk_cid": "object",
                    "pk_partition": "object",
                    "entry_date": "object",
                    "loans": "uint8",
                    "mortgage": "uint8",
                    "long_term_deposit": "uint8",
                    "short_term_deposit": "uint8",
                    "funds": "uint8",
                    "securities": "uint8",
                    "credit_card": "uint8",
                    "pension_plan": "uint8",
                    "payroll_account": "uint8",
                    "emc_account": "uint8",
                    "debit_card": "uint8",
                    "em_acount": "uint8",
                    "active_customer": "uint8",
                    "region": "object",
                    "month_year": "object"})

#apr = pd.read_csv("https://github.com/shogoBCN/pub_data/blob/main/active_per_region.csv?raw=true")
#gdf = gpd.read_file("https://github.com/shogoBCN/pub_data/blob/main/Spain_regions.geojson?raw=true")
#asr = pd.read_csv("https://github.com/shogoBCN/pub_data/blob/main/all_sales_region.csv?raw=true")
#prod_sales_12 = pd.read_csv("https://github.com/shogoBCN/pub_data/blob/main/sales_12.csv?raw=true")
#prod_sales_6 = pd.read_csv("https://github.com/shogoBCN/pub_data/blob/main/sales_6.csv?raw=true")
#prod_sales_3 = pd.read_csv("https://github.com/shogoBCN/pub_data/blob/main/sales_3.csv?raw=true")

table_dist_dict = [ {"label": item, "value": item} for item in ["All Users", "New Users", "Stock Users"] ]
region_dict = [{"label": region, 'value': region} for region in asr["region"].unique()]
products = ["short_term_deposit", "loans", "mortgage", "funds","securities", "long_term_deposit", "credit_card", "pension_plan", "payroll_account", "emc_account", "debit_card", "em_acount"]
KPI_one_df = df_bob.groupby("pk_partition")["active_customer"].mean().reset_index()
KPI_two_1 = df_bob.groupby(["pk_partition"])[products].sum()
KPI_two_1["total_products"] = KPI_two_1[products].sum(axis=1)
KPI_two_2 = df_bob.groupby(["pk_partition"])[products].mean()
KPI_two_2["mean_products"] = KPI_two_2[products].sum(axis=1)

### MAP
gdf_fig = px.choropleth_mapbox(
    gdf, 
    geojson = gdf.geometry, 
    locations = gdf.index,
    color_continuous_scale = colors.sequential.Greens,
    color = "Σ Users",
    mapbox_style = "carto-positron",
    zoom = 4, 
    center = {"lat": 40.416775, "lon": -3.7037},
    opacity = 0.45,
    labels = {'value':'Value'},
    height = 250)
gdf_fig.update_layout(dict( margin = dict(l = 0, r = 0, t = 0, b = 0)))

### KPI ONE ( C A R )
kpi_one_fig = px.line(KPI_one_df, x = "pk_partition", y = "active_customer", color_discrete_sequence = ["MediumSeaGreen"])
kpi_one_fig.add_shape(type = "line", x0 = KPI_one_df["pk_partition"].min(), y0 = 0.5, x1 = KPI_one_df["pk_partition"].max(), y1 = 0.5,
              line = dict(color = "#0B5345", width = 2, dash = "dash"))
kpi_one_fig.update_layout(
    title = dict(text = "Customer Activity Rate (CAR)", x = 0.5),
    yaxis = dict(title = "Application Activity in %", range = [0.325, 0.6]), xaxis_title = "",
    height = 400, autosize = True,
    margin = {'t': 32, "b": 10, "l": 2, "r": 2},
    legend = dict(orientation = "h", yanchor = "bottom", y = 1.02, xanchor = "right", x = 1))
kpi_one_fig.add_annotation(x = KPI_one_df["pk_partition"][3], y = 0.52, text = "50% Threshold Line",
                   showarrow = False, font = dict(color = "#0B5345", size = 14))

### KPI TWO ( A P C )
KPI_Two_fig = go.Figure()
KPI_Two_fig.add_trace(go.Scatter(x = KPI_two_1.index, y = KPI_two_1["total_products"], name = "Total Products", line = dict(color = "MediumSeaGreen")))
KPI_Two_fig.add_trace(go.Scatter(x = KPI_two_2.index, y = KPI_two_2["mean_products"], name = "Mean Products", yaxis = "y2", line = dict(color = "#E67E22")))
KPI_Two_fig.update_layout(
    title = dict(text = "Average Number of Products per Customer (APC)", x = 0.5),
    yaxis = dict(title = "Accumulative Σ of Products"),
    yaxis2 = dict(title="Ø Products per User", overlaying = "y", side = "right"),
    height = 400, autosize = True,
    margin = {'t': 67, "b": 10, "l": 2, "r": 2},
    legend = dict(orientation = "h", yanchor = "bottom", y = 1.02, xanchor = "right", x = 1))


