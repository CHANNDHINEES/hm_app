import sys
import dash_bootstrap_components as dbc
import requests
from dash import dcc, html, State
from app import app
import logging
from dash_extensions.enrich import Output, Input
from pages.splash_screen_patient import splash_screen_patient
from pages.splash_screen_staff import splash_screen_staff
from pages.login import login
from pages.submit_stats import submit_stats
from pages.register_patients import register_patients
from utils.constants import REDIRECT_URI, CLIENT_ID, TOKEN_URL, USER_INFO_URL
from datetime import datetime, timedelta
from pages.view_history.view_history import view_history
from pages.patient_records import patient_records
from pages.deregister_patients import deregister_patient
server = app.server

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logo_path = 'assets/logo.jpg'

navbar = dbc.Navbar(
    children=[
            dbc.Row(
                [
                    dbc.Col(html.A(html.Img(src=logo_path, height="75px",
                                     style={"marginLeft": "20px"}),
                           href="/home",
                           )),
                    dbc.Col(html.A(dbc.NavbarBrand("Remote Patient Monitoring",
                                            className="ms-2",
                                            style={"marginLeft": "20px"}),
                           href="/home")),
                    dbc.Col(html.Div(id="login-status")),
                    dcc.Store(id="session-store", data=None,
                              storage_type="local")


                ],
                align="center",
                className="g-0",
            ),

    ],

    color="primary",
    dark=True,
    sticky=True,
    id="navbar",

)

content = html.Div(id="page-content",
                   style={"padding": "0px", "margin": "0px"})

review_error_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Review not found"), close_button=True),
        dbc.ModalBody(
            [
                html.Div(id="review-error-modal-body",
                         style={"text-align": "left"}),
                html.Br(),
            ]
        ),
    ],
    id="review-error-modal",
    is_open=False,
    size="lg",
    scrollable=True,
)

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        navbar,
        content,
    ]
)


@app.callback(
    [
        Output("page-content", "children"),
        Output("session-store", "data")
    ],
    [Input("url", "pathname"),
     State("url", "href"),
     State("session-store", "data")
     ],
)
def render_page_content(pathname, href, existing_session_store):
    """
    Description:
        routing
    Arguments:
        pathname
    Returns: content of page
    """
    if REDIRECT_URI in href:
        try:
            authorization_code = href.split('?')[1].split('=')[1]
            token_response = requests.post(
                TOKEN_URL,
                data={
                    'grant_type': 'authorization_code',
                    'client_id': CLIENT_ID,
                    'code': authorization_code,
                    'redirect_uri': REDIRECT_URI
                },
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            )
            if token_response.status_code == 200:
                token_data = token_response.json()
                access_token = token_data.get('access_token')
                refresh_token = token_data.get('refresh_token')
            else:
                access_token = None
                refresh_token = None
            if access_token and refresh_token:
                userinfo_response = requests.get(
                    USER_INFO_URL,
                    headers={'Authorization': f'Bearer {access_token}'}
                )
                userinfo = userinfo_response.json()
                session_data = {
                    'access_token': access_token,
                    'email': userinfo.get('email'),
                    'name':userinfo.get('name'),
                    'user_type': userinfo.get('custom:usertype'),
                    'nric': userinfo.get('custom:nric'),
                    'expires_at': datetime.utcnow() + timedelta(seconds=3600),
                    'refresh_token': refresh_token
                }
                existing_session_store = session_data
        except:
            pass
    if existing_session_store and existing_session_store['access_token'] and existing_session_store['user_type']:
        if pathname == "/":
            return login.layout, existing_session_store
        if existing_session_store['user_type'] == "patient":
            # print(nric)
            if pathname == "/home":
                    return splash_screen_patient.layout, existing_session_store
            elif pathname == "/patient/submit-stats":
                return submit_stats.layout, existing_session_store
            elif pathname == "/patient/view-history":
                return view_history(existing_session_store['nric']), existing_session_store
            else:
                return dbc.Alert("404: Not found",
                                 color="danger"), existing_session_store
        elif existing_session_store['user_type'] == "staff":
            if pathname == "/home":
                return splash_screen_staff.layout, existing_session_store
            elif pathname == "/staff/register-patients":
                return register_patients.layout, existing_session_store
            elif pathname == "/staff/search-pat-records":
                return patient_records.layout,existing_session_store
            elif pathname == "/staff/de-register-patients":
                return deregister_patient.layout,existing_session_store
            else:
                return dbc.Alert("404: Not found",
                                 color="danger"), existing_session_store
    else:
        return login.layout, existing_session_store


if __name__ == "__main__":
    port = 8080
    if len(sys.argv) > 1:
        port = sys.argv[1]
    app.run_server(
        port=port,
        debug=True,
        dev_tools_ui=True,
        dev_tools_props_check=False,
    )
