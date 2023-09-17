from dash import dcc, html
from components import FormRow
import dash_bootstrap_components as dbc

from utils.constants import AUTHORIZATION_URL

login_id_control = dcc.Input(
    id="login-id",
    type="text",
    value="",
    placeholder="login id",
    className="form-control",
    debounce=True,
)

login_id_row = FormRow(
    name="name-row",
    text=html.Div(
        [
            html.Span("Login ID"),
            html.Span(
                "*", style={"color": "red"}, id="login-id-required"
            ),
        ]
    ),
    control=login_id_control,
    html_for="login-id",

)

pwd_control = dcc.Input(
    id="pwd",
    type="text",
    value="",
    placeholder="password",
    className="form-control",
    debounce=True,
)

pwd_row = FormRow(
    name="name-row",
    text=html.Div(
        [
            html.Span("Password"),
            html.Span(
                "*", style={"color": "red"}, id="pwd-required"
            ),
        ]
    ),
    control=pwd_control,
    html_for="pwd",

)


save_row = html.Div(
    [

        dbc.Button("Login", id="submit-button", className="me-md-2", href=AUTHORIZATION_URL),
        # dbc.Button("Forgot ?", id="forgot-button", className="me-md-2"),
    ],
    style={
        "width": "auto",
        "margin": "0 auto",
        "text-align": "center",
        "justify-content": "center",
    },
)

layout = html.Div(
    [
        # dbc.Card(
        #     [
                dbc.CardBody(
                    [
                        dbc.Container(
                            children=html.Div(
                                [
                                    dbc.Form(
                                        id="form-new-product",
                                        children=[
                                            # login_id_row,
                                            # pwd_row,
                                            save_row,

                                        ],
                                    )
                                ],
                                id="login-page",
                                style={"display": "inline"},
                            ),
                        )
                    ]
                ),
        #     ]
        # )
    ],
    style={"padding": "10px", "display": "inline"},
)