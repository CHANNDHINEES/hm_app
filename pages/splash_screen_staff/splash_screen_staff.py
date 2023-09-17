from dash import html
import dash_bootstrap_components as dbc

# The first screen that is loaded allowing reviews to be created or loaded
column_styles = {"margin": "auto", "textAlign": "center"}
layout = dbc.Container(
    html.Div(
        [
            dbc.Row(
                dbc.Col(
                    [
                        html.H1(
                            "Welcome to Patient Self Help systems",
                            style={"paddingBottom": "30px"},
                            id="username",
                        ),
                        html.H4("What do you want to do?"),
                    ],
                    style=column_styles,
                ),
                style={"paddingBottom": "50px"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button("Patient Records", href="staff/search-pat-records"),
                        style=column_styles,
                    ),
                    dbc.Col(
                        dbc.Button("Register Patients", href="staff/register-patients"),
                        style=column_styles,
                    ),
                    dbc.Col(
                        dbc.Button("De-register Patients", href="staff/de-register-patients"),
                        style=column_styles,
                    ),

                ]
            ),
        ],
        style={"marginTop": "15vh"},
    ),
    style={"height": "90vh", "width": "50vw"},
)
