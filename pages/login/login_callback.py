from dash.exceptions import PreventUpdate

from utils.constants import REDIRECT_URI
from dash.dependencies import Input, Output, State
from app import app
from authlib.integrations.requests_client import OAuth2Session, oauth2_session


@app.callback(Output("login-status", "children"), Input("url", "pathname"))
def handle_callback(href):
    if REDIRECT_URI in href:
        access_token = href.split('access_token=')[1].split('&')[0]
        if access_token:
            userinfo_response = oauth2_session.get(
                'https://rpm.auth.ap-southeast-2.amazoncognito.com/oauth2/userInfo')
            userinfo = userinfo_response.json()
            app.session['access_token'] = access_token
            app.session['email'] = userinfo.get('email')
            return f"User is logged in as {userinfo.get('email')}"
        else:
            return "Login failed"
    else:
        raise PreventUpdate







