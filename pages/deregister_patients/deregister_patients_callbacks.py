import json
import requests
import pandas as pd
from dash import html, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from pages.register_patients.register_patients_callbacks import create_user
from pages.view_history.view_history import view_history
from app import app


def retrieve_patient(clinic_id, patient_id):
    # Define the API URL
    if clinic_id and patient_id:
        api_url = "https://ax6rdgbii4.execute-api.ap-southeast-1.amazonaws.com/prod/patientdetails"
        payload = json.dumps({
            "operation": "Get",
            "payload": {
                "CLINICCODE": clinic_id,
                "NRIC": patient_id
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST",
                                    api_url,
                                    headers=headers,
                                    data=payload)
        if response.status_code == 200:
            data = response.json()
            # Assuming the response contains a list of patient records, you can convert it to a DataFrame
            df = pd.DataFrame(data)
            if df.shape[0] == 0:
                raise Exception("User not found")
            else:
                return df
        else:
            raise Exception("User not found")
    else:
        raise Exception("Both Clinic id and Patient id is required")

    # Make the API request


@app.callback(
    Output('deregister-patient-result-display', 'children'),
    Input('deregister-find-user-button', 'n_clicks'),
    State('deregister-find-patient-id', 'value'),
    State('deregister-find-clinic-id', 'value'),
    prevent_initial_call=True
)
def deregister_patients(n_clicks, patient, clinic):
    if n_clicks:
        try:
            response = retrieve_patient(clinic, patient)
            if response['Status'][0] == 'Inactive':
                raise Exception("User already Inactive")
            response2 = create_user(clinic_code=clinic,
                                    nric=patient,
                                    full_name=response['Name'][0],
                                    gender=response['Gender'][0],
                                    age=response['Age'][0],
                                    others=response['Others'][0],
                                    status='Inactive',
                                    remarks=response['Remarks'][0])
            return f'deregistered the user:{patient}'
        except Exception as e:  # work on python 2.x
            return 'Failed: ' + str(e)
    raise PreventUpdate


@app.callback(
    [Output('deregister-patient-result-display', 'children')],
    Input('deregister-find-user-reset-button', 'n_clicks'),
    prevent_initial_call=True
)
def reset_find_patients(n_clicks):
    if n_clicks:
        return [None]

    raise PreventUpdate
