import dash
import dash_bootstrap_components as dbc
from dash import html, ALL
from dash.exceptions import PreventUpdate
from dash import dcc, Input, Output, State
import logging


class CategoryListSelector(html.Div):
    box_style = {
        "height": "190px",
        "border": "1px lightgray solid",
        "borderRadius": "5px",
        "overflowY": "auto",
        "marginTop": "15px",
        "font-size": "14px",
    }

    def __init__(
        self,
        app,
        name,
        categories_data_func,
        options_data_func,
        value_store_id,
        descriptions_data_func,
        default_options_func,
        inputs=None,
        category_column="Category",
        display_name_column="Display Name",
        field_name_column="Field Name",
        add_all=True,
        display_heading=None,
        **kwargs,
    ):
        self.mod_name = kwargs.copy()
        logging.info(f"Invoked Category Selection from module {self.mod_name}")
        if "mod_name" in kwargs.keys():
            super().__init__(kwargs.pop("mod_name"))
        else:
            super().__init__(**kwargs)

        category_dropdown_control = html.Div(
            dcc.Dropdown(
                id=f"{name}-dropdown",
                multi=True,
                searchable=False,
                clearable=False,
                persistence=False,
                value=None,
            ),
            id=f"{name}-options-loader",
        )
        options_listbox = html.Div(
            id=f"{name}-options",
            style=CategoryListSelector.box_style,
        )
        selected_listbox = html.Div(
            id=f"{name}-selected-options-panel",
            style=CategoryListSelector.box_style,
        )
        clear_all_button = dbc.Button(
            "Clear All",
            id=f"{name}-clear-all",
            size="sm",
            style={
                "margin-top": "10px",
            },
        )
        year_checklist = dbc.Checklist(
            options=[
                {
                    "label": "TY",
                    "value": "TY",
                },
                {
                    "label": "LY",
                    "value": "LY",
                },
            ],
            inline=True,
            id="year-checklist-input",
        )
        period_checklist = dbc.Checklist(
            options=[
                {
                    "label": "13WK",
                    "value": "13",
                },
                {
                    "label": "26WK",
                    "value": "26",
                },
                {
                    "label": "52WK",
                    "value": "52",
                },
            ],
            inline=True,
            id="period-checklist-input",
        )

        self.children = html.Div(
            [
                html.H4(display_heading) if display_heading else None,
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Label("Filter Category"),
                            width=7,
                        ),
                    ],
                ),
                dbc.Row(category_dropdown_control),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Input(
                                id="search_input",
                                type="text",
                                value="",
                                placeholder="Search",
                                className="form-control",
                                style={"padding": "0.4rem 1rem"},
                            ),
                            style={"marginTop": "10px", "paddingRight": "30px"},
                            width=5,
                        ),
                        dbc.Col(
                            year_checklist,
                            style={"marginTop": "10px"},
                            width=2,
                        ),
                        dbc.Col(
                            period_checklist,
                            style={"marginTop": "10px"},
                            width=3,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(options_listbox),
                        dbc.Col(
                            [
                                html.Div(selected_listbox),
                                html.Div(clear_all_button),
                            ],
                        ),
                    ]
                ),
                dcc.Interval(id=f"{name}-loader", max_intervals=1, interval=10),
            ]
        )

        self.name = name
        if not isinstance(inputs, list) and inputs is not None:
            inputs = [inputs]
        self.inputs = inputs
        self.category_column = category_column
        self.display_name_column = display_name_column
        self.field_name_column = field_name_column
        self.value_store_id = value_store_id
        self.categories_data_func = categories_data_func
        self.options_data_func = options_data_func
        self.description_data_func = descriptions_data_func
        self.default_options_func = default_options_func
        self.register_callback(app)

    def register_callback(self, app):
        category_inputs = [Input(f"{self.name}-loader", "value")]
        if self.inputs is not None:
            category_inputs = self.inputs

        app.callback(
            Output(f"{self.name}-options-loader", "children"), category_inputs
        )(self.load_categories)

        load_option_inputs = [
            Input(f"{self.name}-dropdown", "value"),
            Input(f"year-checklist-input", "value"),
            Input(f"period-checklist-input", "value"),
            Input(f"search_input", "value"),
            State(f"{self.name}-dropdown", "options"),
        ]

        if self.inputs is not None:
            load_option_inputs = load_option_inputs + self.inputs

        app.callback(Output(f"{self.name}-options", "children"), load_option_inputs)(
            self.load_options
        )

        app.callback(
            Output(self.value_store_id, "data"),
            Input(
                {
                    "role": f"{self.name}-option",
                    "option-value": ALL,
                    "option-label": ALL,
                },
                "n_clicks",
            ),
            State(self.value_store_id, "data"),
        )(self.add_option)

        app.callback(
            Output(self.value_store_id, "data"),
            Input(
                {
                    "role": f"{self.name}-remove-option",
                    "option-value": ALL,
                    "option-label": ALL,
                },
                "n_clicks",
            ),
            State(self.value_store_id, "data"),
        )(self.remove_option)

        app.callback(
            Output(f"{self.name}-selected-options-panel", "children"),
            Input(self.value_store_id, "data"),
        )(self.load_selected_options)

    def clear_selected_items(self, n_clicks, options, selected_items):
        if n_clicks:
            return None
        return dash.no_update

    def load_categories(self, *args):
        options = (
            self.categories_data_func()
            if self.inputs is None
            else self.categories_data_func(*args)
        )

        # Set default value to None for New review
        if self.mod_name["mod_name"] == "New Review":
            value = None
        else:
            value = options[0] if len(options) > 0 else None

        # Iterate over the options list if not empty
        opts = [{"label": x, "value": x} for x in options] if options else []

        return dcc.Dropdown(
            id=f"{self.name}-dropdown",
            options=opts,
            multi=True,
            searchable=True,
            clearable=False,
            persistence=False,
            value=value,
        )

    def load_options(
        self, selected_value, year, period, search_input, all_category_options, *args
    ):
        if (year or period or search_input) and not selected_value:
            selected_value = [i["value"] for i in all_category_options]
        if selected_value:
            options = self.options_data_func(selected_value, *args)
            descriptions = (
                self.description_data_func(selected_value, *args)
                if self.description_data_func is not None
                else None
            )
            if year:
                temp_options = {}
                for i in options.keys():
                    for j in year:
                        if j in i:
                            temp_options[i] = options[i]
                options = temp_options

            if period:
                temp_options = {}
                for i in options.keys():
                    for j in period:
                        if j in i:
                            temp_options[i] = options[i]
                options = temp_options

            if search_input:
                temp_options = {}
                option_dict_keys = list(options.keys())
                option_dict_values = list(options.values())

                for i in range(len(option_dict_keys)):
                    if (
                        search_input.lower() in option_dict_keys[i].lower()
                        or search_input.lower() in option_dict_values[i].lower()
                        # or search_input.lower()
                        # in descriptions[option_dict_keys[i]].lower()
                    ):
                        temp_options[option_dict_keys[i]] = option_dict_values[i]
                options = temp_options

            layout = dbc.Card(
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem(
                            f"+ {options[value]}",
                            class_name="hover-list-group-item",
                            id={
                                "role": f"{self.name}-option",
                                "option-value": value,
                                "option-label": options[value],
                            },
                        )
                        for value in options
                    ]
                    + [
                        dbc.Tooltip(
                            id={
                                "role": f"{self.name}-tooltip",
                                "option-value": value,
                                "option-label": options[value],
                            },
                            children=descriptions[value]
                            if descriptions is not None
                            else None,
                            placement="left",
                            target={
                                "role": f"{self.name}-option",
                                "option-value": value,
                                "option-label": options[value],
                            },
                        )
                        for value in options
                        if descriptions is not None
                    ],
                    flush=True,
                )
            )

            # Return an empty array to clear the selected metrics on load of the component
            return layout
        else:
            layout = dbc.Card(
                dbc.ListGroup(
                    [],
                    flush=True,
                )
            )
            return layout

    def load_selected_options(self, selected):
        default_options = self.default_options_func()
        if selected is not None:
            layout = dbc.Card(
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem(
                            f"- {selected[value]}",
                            class_name="hover-list-group-item",
                            id={
                                "role": f"{self.name}-remove-option",
                                "option-value": value,
                                "option-label": selected[value],
                            },
                        )
                        for value in selected
                    ]
                    + [
                        dbc.ListGroupItem(
                            f"(Default) {default_options[value]}",
                            class_name="hover-list-group-item",
                            id={
                                "role": f"{self.name}-default-option",
                                "option-value": value,
                                "option-label": default_options[value],
                            },
                            style={"color": "blue"},
                        )
                        for value in default_options
                    ],
                    flush=True,
                )
            )
            return layout
        else:
            raise PreventUpdate

    def add_option(self, n_clicks, current_selected_options):
        triggered = dash.callback_context.triggered
        if current_selected_options is None:
            current_selected_options = {}
        if len(triggered) > 0 and any(n_clicks):
            for trigger in triggered:
                info = eval(trigger["prop_id"].replace(".n_clicks", ""))
                value = info["option-value"]
                label = info["option-label"]
                current_selected_options[value] = label
            return current_selected_options
        raise PreventUpdate

    def remove_option(self, n_clicks, current_selected_options):
        triggered = dash.callback_context.triggered
        if current_selected_options is None:
            current_selected_options = {}
        if len(triggered) > 0 and any(n_clicks):
            for trigger in triggered:
                value = eval(trigger["prop_id"].replace(".n_clicks", ""))[
                    "option-value"
                ]
                del current_selected_options[value]
            return current_selected_options
        raise PreventUpdate
