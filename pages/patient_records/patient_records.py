from dash import dcc, html
from components import FormRow
import dash_bootstrap_components as dbc
from pages.patient_records import patient_records_callback


def get_input_area(object_name, heading, type, place_holder=None):
    control = dcc.Input(
        id=f"{object_name}-id",
        type=type,
        value="",
        placeholder=place_holder,
        className="form-control",
        debounce=True,
        persistence = "memory"
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


patient_id_row = get_input_area("find-patient", "Patient ID", "text", )
clinic_id_row = get_input_area("find-clinic", "Clinic ID*", "text", )

save_row = html.Div(
    [

        dbc.Button("Find", id="find-user-button", className="me-md-2"),
        dbc.Button("Reset", id="find-user-reset-button", className="me-md-2"),
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
                                id="register-patient-form",
                                children=[
                                    clinic_id_row,
                                    patient_id_row,

                                    save_row,
                                    html.Div(id='patient-result-display')
                                ],
                            )
                        ],
                        id="find-patient-page",
                        style={"display": "inline"},
                    ),
                )
            ]
        ),

    ],
    style={"padding": "10px", "display": "inline"},
)
