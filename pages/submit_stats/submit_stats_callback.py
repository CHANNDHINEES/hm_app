import requests
from dash import Output, Input, State
from dash.exceptions import PreventUpdate
from pages.submit_stats import submit_stats

from app import app
import datetime


def submit_patient_record(sys, dia, pulse, temperature,nric,name):
    api_url = "https://yzbuzi7mxi.execute-api.ap-southeast-1.amazonaws.com/prod/vitals"
    if sys or dia or pulse or temperature:
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # Define the JSON payload
        payload = {
            "operation": "Put",
            "payload": {
                "NRIC": f"{nric}",
                "TimeTaken": f"{formatted_datetime}",
                "Name": f"{name}",
                "BPSys": f"{sys}",
                "BPDia": f"{dia}",
                "HR": f"{pulse}",
                "Temperature": f"{temperature}"
            }
        }
        # Make the API request
        response = requests.post(api_url, json=payload)
        return response

    else:
        raise Exception("Enter any value for sys or dia or pulse or temperature")


@app.callback(
    Output('result-message-submit-stats', 'children'),
    Input('submit-button-stats', 'n_clicks'),
    State('sys-id', 'value'),
    State('dia-id', 'value'),
    State('pulse-id', 'value'),
    State('temperature-id', 'value'),
    State('spo2-id', 'value'),
    State("session-store", "data"),
    prevent_initial_call=True
)
def submit_patient_record_callback(n_clicks, sys, dia, pulse, temperature, spo2, existing_session_store):
    if n_clicks:
        try:
            response = submit_patient_record(sys, dia, pulse,
                                             temperature,
                                             existing_session_store['nric'],
                                             existing_session_store['name'])
            return f"Record submitted successfully"
        except Exception as e:
            return 'Failed: ' + str(e)
    else:
        raise PreventUpdate

@app.callback(
    [Output('sys-id', 'value'),
     Output('dia-id', 'value'),
     Output('pulse-id', 'value'),
     Output('temperature-id', 'value'),
     Output('spo2-id', 'value'),
     Output('result-message-submit-stats', 'children')],
    Input("reset-button-stats", 'n_clicks'),
    prevent_initial_call=True
)
def reset_callback(n_clicks):
    if n_clicks:
        return [None, None, None, None, None, None]
    else:
        raise PreventUpdate
