from dash import dcc, html
from components import FormRow
import dash_bootstrap_components as dbc


def get_input_area(object_name, heading, type, place_holder=None):
    control = dcc.Input(
        id=f"{object_name}-id",
        type=type,
        value="",
        placeholder=place_holder,
        className="form-control",
        debounce=True,
    )

    form_row = FormRow(
        name="name-row",
        text=html.Div(
            [
                html.Span(heading),
            ]
        ),
        control=control,
        html_for=f"{object_name}-id",

    )

    return form_row


sys_row = get_input_area("sys", "SYS (mmHg)", "numeric", )
dia_row = get_input_area("dia", "DIA (mmHg)", "numeric", )
pulse_row = get_input_area("pulse", "PULSE (per minute)", "numeric", )
temperature_row = get_input_area("temperature", "Temperature (°C)", "numeric")
spo2_row = get_input_area("spo2", "SpO2 (%)", "numeric",)


save_row = html.Div(
    [

        dbc.Button("Submit", id="submit-button", className="me-md-2"),
        dbc.Button("Reset", id="forgot-button", className="me-md-2"),
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
                                    sys_row,
                                    dia_row,
                                    pulse_row,
                                    temperature_row,
                                    spo2_row,
                                    save_row,
                                ],
                            )
                        ],
                        id="submit-stat-page",
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
