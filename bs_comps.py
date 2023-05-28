from dash import html
import dash_bootstrap_components as dbc
from variables import table_dist_dict

button_group = html.Div(
    className = "radio_group",
    children = [
        dbc.RadioItems(
            id = "user_type_buttons",
            className = "btn_group",
            inputClassName = "btn_check",
            labelClassName = "btn btn_outline_primary",
            labelCheckedClassName = "active",
            options = table_dist_dict,
            value = table_dist_dict[0]["value"],
        )
    ],
)

time_radios = html.Div(
    className = "time_period_selectors",
    children = [
        dbc.RadioItems(
            id = "user_type_buttons_2",
            className = "btn_group",
            inputClassName = "btn_check",
            labelClassName = "btn btn_outline_primary",
            labelCheckedClassName = "active",
            options = [ {"label": item, "value": item} for item in ["1 year", "6 month", "3 month"]],
            value = "1 year",
        )
    ],
)
