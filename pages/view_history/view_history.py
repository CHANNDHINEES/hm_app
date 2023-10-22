import requests
import pandas as pd
from dash import html, dash_table, dcc
import json
from utils.constants import PATIENT_VITALS_API_URL
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def view_history(nric):
    payload = json.dumps({
        "operation": "Get",
        "payload": {
            "NRIC": nric
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST",
                                PATIENT_VITALS_API_URL,
                                headers=headers,
                                data=payload)

    if response.status_code == 200:
        data = response.json()
        # Assuming the response contains a list of patient records, you can convert it to a DataFrame
        df = pd.DataFrame(data)
        df[['BPDia', 'BPSys', 'Temperature', 'HR']] = df[['BPDia', 'BPSys', 'Temperature', 'HR']].apply(
            pd.to_numeric)
        df = df[['TimeTaken','BPDia', 'BPSys', 'Temperature', 'HR']]
        df.columns = ['timestamp','Diastolic BP (mm hg)', 'Systolic BP (mm hg)', 'Temperature (C)', 'Heart rate (per minute)']
        df = df.sort_values(by=['timestamp'],ascending=False)
        fig = make_subplots(rows=2, cols=2)
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['Diastolic BP (mm hg)'],
                                 mode='lines+markers', name='Diastolic BP (mm hg)'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['Systolic BP (mm hg)'],
                                 mode='lines+markers', name='Systolic BP (mm hg)'), row=1, col=2)
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['Temperature (C)'],
                                 mode='lines+markers', name='Temperature (C)'), row=2, col=1)
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['Heart rate (per minute)'],
                                 mode='lines+markers', name='Heart rate (per minute)'), row=2, col=2)

        fig.update_layout(height=600, title_text="User data across time")
        # df = df[['TimeTaken','BPDia', 'BPSys', 'Temperature', 'HR']]
        # df.columns = ['timestamp','Diastolic BP (mm hg)', 'Systolic BP (mm hg)', 'Temperature (C)', 'Heart rate (per minute)']
        output_req = html.Div([dash_table.DataTable(df.to_dict('records'),
                                                    [{"name": i, "id": i} for i in df.columns],
                                                    style_table={'padding': '20px'},
                                                    style_header={'fontWeight': 'bold','text-align': 'left'},
                                                    style_cell={'text-align': 'left'},

                                                    sort_action="native",
                                                    page_action="native",
                                                    page_current=0,
                                                    page_size=5,
                                                    editable=False,
                                                    ),
                               html.Div(children=[
                                   html.Div(dcc.Graph(figure=fig, id="gr0"), className="six columns"),
                               ], className="row")

                               ]
                              )

        return output_req
    else:
        return html.Div(id="patient-records",
                        children="No records found")
