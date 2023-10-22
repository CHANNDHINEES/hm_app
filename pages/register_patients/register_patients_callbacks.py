import boto3
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from utils.constants import USER_POOL_ID, REGION
from app import app
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

boto3.setup_default_session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
)


def create_user(clinic_code, nric, full_name, gender, age, remarks, others, status):
    url = "https://ax6rdgbii4.execute-api.ap-southeast-1.amazonaws.com/prod/patientdetails"
    payload = json.dumps({
        "operation": "Put",
        "payload": {
            "CLINICCODE": clinic_code,
            "NRIC": nric,
            "Name": full_name,
            "Gender": gender,
            "Age": age,
            "Remarks": remarks,
            "Others": others,
            "Status": status
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def create_user_cognito(email, password, full_name, nric,
                        vital_stats_sub = '', device_type = '',
                        device_serial = '', user_type = 'patient'):
    client = boto3.client('cognito-idp', region_name=REGION)
    user_pool_id = USER_POOL_ID
    response = client.admin_create_user(
        UserPoolId=user_pool_id,
        Username=email,
        TemporaryPassword=password,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': email
            },
            {
                'Name': 'name',
                'Value': full_name
            },
            {
                'Name': 'custom:nric',
                'Value': nric
            },
            {
                'Name': 'custom:vital_stats_sub',
                'Value': vital_stats_sub
            },
            {
                'Name': 'custom:device_type',
                'Value': device_type
            },
            {
                'Name': 'custom:device_serial',
                'Value': device_serial
            },
            {
                'Name': 'custom:usertype',
                'Value': user_type
            },

            # Add more user attributes as needed
        ],
        MessageAction='SUPPRESS'  # Suppress sending a welcome email
    )
    return response


@app.callback(
    Output('result-message', 'children'),
    Input('register-user-button', 'n_clicks'),
    State('email-id', 'value'),
    State('full_name-id', 'value'),
    State('nric-id', 'value'),
    # State('vital_stats_sub-id', 'value'),
    # State('device_type-id', 'value'),
    # State('device_serial_number-id', 'value'),
    State('user_type-id', 'value'),
    State('age-id', 'value'),
    State('clinic_code-id', 'value'),
    State('gender-id', 'value'),

)
def add_user_to_cognito(n_clicks, email, full_name,
                        nric,
                        user_type, age, clinic_code, gender):
    if n_clicks:
        try:
            password = "Aa@123456"  # to be random
            response = create_user_cognito(email = email,
                                           password=password,
                                           full_name=full_name,
                                           nric=nric,
                                           user_type = user_type)

            response2 = create_user(clinic_code=clinic_code, nric=nric,
                                    full_name = full_name,
                                    gender = gender,
                                    age = age,
                                    others=None,
                                    status='Active', remarks="Normal")
            return f"User created successfully."
        except Exception as e:  # work on python 2.x
            return 'Failed: ' + str(e)

    raise PreventUpdate
