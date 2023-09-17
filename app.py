"""
creating the app
"""
import dash_bootstrap_components as dbc
from dash_extensions.enrich import DashProxy, MultiplexerTransform

external_stylesheets = [dbc.themes.LUX, dbc.icons.FONT_AWESOME]
external_scripts = ["https://cdn.plot.ly/plotly-2.18.0.min.js"]

app = DashProxy(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    # these meta_tags ensure content is scaled correctly on different devices
    # see: https://www.w3schools.com/css/css_rwd_viewport.asp for more
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    title="RPM",
    update_title="Loading...",
    prevent_initial_callbacks=False,
    transforms=[MultiplexerTransform()],
)

server = app.server
app.config.suppress_callback_exceptions = True