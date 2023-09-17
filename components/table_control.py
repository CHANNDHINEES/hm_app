import dash_bootstrap_components as dbc
from dash import html
from app import app
from components.pagination import Pagination
from components.filter_control import filter_control
from components.sort_dropdown import sort_dropdown

paginator = Pagination(id="paginator", page_number=1)
paginator.register_callback(app)

table_control = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([sort_dropdown], width=2),
                dbc.Col([filter_control], width=8),
                dbc.Col(paginator),
            ],
            align="center",
            style={"height": "80px"},
        )
    ],
    style={"height": "80px", "paddingBottom": "5px", "marginRight": "20px"},
)
