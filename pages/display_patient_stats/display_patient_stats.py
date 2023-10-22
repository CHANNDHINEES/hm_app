from flask import Flask, render_template
import requests
import pandas as pd
from dash import html


def display_patient_details():
    # Define the API URL
    api_url = "https://yzbuzi7mxi.execute-api.ap-southeast-1.amazonaws.com/prod/vitals"

    # Define the JSON payload
    payload = {
        "operation": "Get",
        "payload": {
            "NRIC": "S1234567G"
        }
    }

    # Make the API request
    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        # Convert the JSON response to a Python dictionary
        data = response.json()

        # Assuming the response contains a list of patient records, you can convert it to a DataFrame
        df = pd.DataFrame(data)
        html_table = df.to_html(classes='table table-striped', index=False)

        output_req = html.Div([
            html.Iframe(
                # enable all sandbox features
                # see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe
                # this prevents javascript from running inside the iframe
                # and other things security reasons
                sandbox='',
                srcDoc=f"""{html_table}"""
            )
        ])
        return output_req
    else:
        return f"Error: {response.status_code}"


layout = display_patient_details()
