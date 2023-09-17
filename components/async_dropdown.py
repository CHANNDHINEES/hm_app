from dash import html
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output
import logging


class AsyncDropdown(html.Div):
    def __init__(
        self,
        name,
        data_function,
        multi=None,
        persistence=None,
        persistence_type=None,
        app=None,
        inputs=None,
        value=None,
        **kwargs,
    ):
        self.mod_name = kwargs.copy()
        logging.info(f"Invoked AsyncDropdown from module {self.mod_name}")
        if "mod_name" in kwargs.keys():
            super().__init__(kwargs.pop("mod_name"))
        else:
            super().__init__(**kwargs)

        self.dropdown = dcc.Dropdown(
            id=f"{name}-id",
            # className="form-select shadow-primary",
            multi=multi,
            value=value,
            persistence=persistence,
            persistence_type=persistence_type,
        )

        internal_children = [self.dropdown]
        if inputs is None:
            internal_children.append(
                dcc.Interval(id=f"{name}-loader", max_intervals=1, interval=10)
            )

        self.children = [html.Div(internal_children, id=f"{name}-output")]

        self.name = name
        self.inputs = inputs
        self.data_function = data_function

        if app is not None:
            self.register_callback(app)

    def register_callback(self, app):
        if self.inputs is None:
            inputs = Input(f"{self.name}-loader", "n_intervals")
        else:
            inputs = self.inputs

        app.callback(Output(f"{self.name}-output", "children"), inputs)(self.load)

    def load(self, *args):
        if self.inputs is None:
            data = self.data_function()
        else:
            data = self.data_function(*args)
        return dcc.Dropdown(
            id=f"{self.name}-id",
            multi=self.dropdown.multi,
            # className="form-select shadow-primary",
            value=data[0]
            if data
            and self.name == "date"
            and self.mod_name
            and self.mod_name["mod_name"] == "New Review"
            else self.dropdown.value,
            persistence=self.dropdown.persistence,
            persistence_type=self.dropdown.persistence_type,
            options=[{"label": x, "value": x} for x in data],
        )
