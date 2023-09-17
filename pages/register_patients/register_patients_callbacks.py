import boto3
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from utils.constants import USER_POOL_ID, REGION
from app import app

from dotenv import load_dotenv
import os

load_dotenv()


boto3.setup_default_session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def create_user(email, password, full_name, nric, vital_stats_sub, device_type,
                device_serial, user_type):
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
    State('vital_stats_sub-id', 'value'),
    State('device_type-id', 'value'),
    State('device_serial_number-id', 'value'),
    State('user_type-id', 'value'),

)
def add_user_to_cognito(n_clicks, email, full_name,
                        nric, vital_stats_sub, device_type,
                        device_serial, user_type):
    if n_clicks:
        try:
            password = "Aa@123456"  # to be random
            response = create_user(email, password, full_name,
                                   nric, vital_stats_sub, device_type,
                                   device_serial, user_type)
            return f"User created successfully."
        except Exception as e:  # work on python 2.x
            return('Failed: ' + str(e))

    raise PreventUpdate
