import requests
import pandas as pd
from dash import html, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from pages.view_history.view_history import view_history

from app import app


def find_patient(clinic_id, patient_id):
    # Define the API URL
    api_url = "https://ax6rdgbii4.execute-api.ap-southeast-1.amazonaws.com/prod/patientdetails"
    response = None
    if patient_id and clinic_id:
        return view_history(patient_id)

    elif clinic_id:
        payload = {
            "operation": "GetList",
            "payload": {
                "CLINICCODE": clinic_id
            }
        }
        response = requests.post(api_url, json=payload)
        if response and response.status_code == 200:
            # Convert the JSON response to a Python dictionary
            data = response.json()
            # Assuming the response contains a list of patient records, you can convert it to a DataFrame
            df = pd.DataFrame(data)
            req_columns = sorted(list(df.columns))
            df = df[req_columns]
            return html.Div(dash_table.DataTable(df.to_dict('records'),
                                 [{"name": i, "id": i} for i in df.columns],
                                 style_table={'padding': '20px'},
                                 style_header={'fontWeight': 'bold', 'text-align': 'left'},
                                 style_cell={'text-align': 'left'},
                                 sort_action="native",
                                 page_action="native",
                                 page_current=0,
                                 page_size=5,
                                 editable=False,
                                 ))
        else:
            return html.Div(f"Error: {response.status_code}")
    else:
        raise Exception("Clinic ID is mandatory")

    # Make the API request


@app.callback(
    Output('patient-result-display', 'children'),
    Input('find-user-button', 'n_clicks'),
    State('find-patient-id', 'value'),
    State('find-clinic-id', 'value'),
    prevent_initial_call=True
)
def find_patients(n_clicks, patient, clinic):
    if n_clicks:
        try:
            response = find_patient(clinic, patient)
            return response
        except Exception as e:  # work on python 2.x
            return 'Failed: ' + str(e)
    raise PreventUpdate


@app.callback(
    [Output('patient-result-display', 'children')],
    Input('find-user-reset-button', 'n_clicks'),
    prevent_initial_call=True
)
def reset_find_patients(n_clicks):
    if n_clicks:
        return [None]

    raise PreventUpdate
