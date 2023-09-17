from dash import dcc, html
from components import FormRow
import dash_bootstrap_components as dbc
from pages.register_patients import register_patients_callbacks

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

email_row = get_input_area("email", "Email Name", "text", )
full_name_row = get_input_area("full_name", "Full Name", "text", )
contact_number_row = get_input_area("contact_number", "Contact Number", "text", )
patient_id_row = get_input_area("nric", "NRIC", "text", )
vital_stats_sub_row = get_input_area("vital_stats_sub", "Vital Stats Submission Mode", "text", )
device_type_row = get_input_area("device_type", "Device Type", "text", )
device_serial_number_row = get_input_area("device_serial_number", "Device Serial Number", "text", )
user_type_row = get_input_area("user_type", "User Type", "text", )


save_row = html.Div(
    [

        dbc.Button("Register", id="register-user-button", className="me-md-2"),
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
                                id="register-patient-form",
                                children=[
email_row,
                                    full_name_row,
                                    contact_number_row,
                                    patient_id_row,
                                    vital_stats_sub_row,
                                    device_type_row,
                                    device_serial_number_row,
                                    user_type_row,
                                    save_row,
                                    html.Div(id='result-message')
                                ],
                            )
                        ],
                        id="register-patient-page",
                        style={"display": "inline"},
                    ),
                )
            ]
        ),

    ],
    style={"padding": "10px", "display": "inline"},
)
