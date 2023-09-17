from dash import html, Output, Input, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


class Pagination(html.Div):
    def __init__(self, page_number=1, *args, **kwargs):
        children = dbc.ButtonGroup(
            [
                dbc.Button(
                    "<", outline=True, color="primary", id="last-page", disabled=True
                ),
                html.Span(
                    "Loading ...",
                    style={"padding": "10px", "marginTop": "5px"},
                    id="page-number-display",
                ),
                dbc.Button(
                    ">", outline=True, color="primary", id="next-page", disabled=True
                ),
            ],
            style={"float": "right"},
        )

        super().__init__(children, *args, **kwargs)
        self.page_number = page_number
        self._prop_names.append("page_number")

    def register_callback(self, app):
        app.callback(
            Output("paginator", "page_number"),
            Input("next-page", "n_clicks"),
            State("paginator", "page_number"),
        )(self.next_page)

        app.callback(
            Output("paginator", "page_number"),
            Input("last-page", "n_clicks"),
            State("paginator", "page_number"),
        )(self.last_page)

    @staticmethod
    def last_page(n_clicks, page_number):
        if n_clicks is None or page_number == 1:
            raise PreventUpdate

        return page_number - 1

    @staticmethod
    def next_page(n_clicks, page_number):
        if n_clicks is None:
            raise PreventUpdate

        return page_number + 1
