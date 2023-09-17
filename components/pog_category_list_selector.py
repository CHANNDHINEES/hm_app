import dash
import dash_bootstrap_components as dbc
from dash import html, ALL
from dash.exceptions import PreventUpdate
from dash import dcc, Input, Output, State
import logging
import dash_daq as daq

from models.pog_category import POGCategory


class POGCategoryListSelector(html.Div):
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
        subcategories_data_func,
        options_data_func,
        value_store_id,
        descriptions_data_func,
        inputs=None,
        category_column="Category",
        display_name_column="Display Name",
        field_name_column="Field Name",
        add_all=True,
        display_heading=None,
        disable_banner=False,
        **kwargs,
    ):
        exclude_no_cluster = daq.BooleanSwitch(
            id=f"{name}-pog-no-cluster-toggle",
            on=True,
            style={"display": "flex", "justify-items": "flex-start"},
        )
        disable_banner = disable_banner if disable_banner else False
        banner_options = [
            {"label": "Dan Murphy's", "value": "DM", "disabled": disable_banner},
            {"label": "BWS", "value": "BWS", "disabled": disable_banner},
        ]

        banner_control = html.Div(
            [
                dbc.RadioItems(
                    id=f"{name}-pog-brand-id",
                    options=banner_options,
                    value="DM",
                    className="btn-group btn-group-sm",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary btn-sm",
                    labelCheckedClassName="active",
                    inputStyle={
                        "paddingLeft": "0px",
                        "line-height": "0.5rem",
                    },
                    persistence=True,
                    persistence_type="session",
                ),
            ],
            className="radio-group",
        )
        category_dropdown_control = html.Div(
            dcc.Dropdown(
                id=f"{name}-pog-dropdown-category",
                multi=False,
                searchable=False,
                clearable=False,
                persistence=False,
                value=None,
            ),
            id=f"{name}-pog-options-loader-category",
        )

        subcategory_dropdown_control = html.Div(
            dcc.Dropdown(
                id=f"{name}-pog-dropdown-subcategory",
                multi=True,
                searchable=False,
                clearable=False,
                persistence=False,
                value=None,
            ),
            id=f"{name}-pog-options-loader-subcategory",
        )

        subcategory_select_dropdown_control = html.Div(
            dcc.Dropdown(
                id=f"{name}-pog-dropdown-subcategory-select",
                multi=True,
                searchable=False,
                clearable=False,
                persistence=False,
                value=None,
            ),
            id=f"{name}-pog-options-loader-subcategory-select",
        )

        pogcategory_options_listbox = html.Div(
            id=f"{name}-pog-options-panel",
            style=POGCategoryListSelector.box_style,
        )
        pogcategory_selected_listbox = html.Div(
            id=f"{name}-pog-selected-options-panel",
            style=POGCategoryListSelector.box_style,
        )
        add_clear_button = dbc.Button(
            f"{'Add' if add_all else 'Clear'} All",
            size="sm",
            id=f"{name}-pog-{'add' if add_all else 'clear'}-all",
            style={
                "margin-top": "10px",
            },
        )
        self.mod_name = kwargs.copy()
        logging.info(f"Invoked Category Selection from module {self.mod_name}")
        if "mod_name" in kwargs.keys():
            super().__init__(kwargs.pop("mod_name"))
        else:
            super().__init__(**kwargs)

        self.children = html.Div(
            [
                html.Span(html.H4(display_heading)) if display_heading else None,
                dbc.Row(dbc.Col(dbc.Label("Retail Brand"))),
                dbc.Row(
                    dbc.Col(banner_control),
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [dbc.Label("Filter Category"), category_dropdown_control],
                        ),
                        dbc.Col(
                            [dbc.Label("Exclude 'NO-CLUSTER'"), exclude_no_cluster],
                            width=4,
                            style={"marginLeft": "10px"},
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("Filter Sub-Category"), width=2),
                        dbc.Col(
                            dbc.Checklist(
                                options=[
                                    {
                                        "label": "Include All",
                                        "value": 1,
                                    },
                                ],
                                id=f"{name}-include-all-checklist-input",
                                className="form-check shadow-primary",
                            )
                        ),
                    ]
                ),
                dbc.Row(subcategory_dropdown_control),
                dbc.Row(
                    [
                        dbc.Col(pogcategory_options_listbox),
                        dbc.Col(
                            [
                                html.Div(pogcategory_selected_listbox),
                                html.Div(add_clear_button),
                            ],
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        html.Span(html.H4("SELECT SUB-CATEGORIES TO DISPLAY")),
                    ]
                ),
                dbc.Row(subcategory_select_dropdown_control),
                dbc.Button(
                    "Add All",
                    size="sm",
                    id=f"{name}-include-all-checklist-input-select",
                    style={
                        "margin-top": "10px",
                    },
                ),
                dbc.Button(
                    "Clear All",
                    size="sm",
                    id=f"{name}-include-all-clear-checklist-input-select",
                    style={
                        "margin-top": "10px",
                        "margin-left": "10px",
                    },
                ),
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
        self.subcategories_data_func = subcategories_data_func
        self.options_data_func = options_data_func
        self.description_data_func = descriptions_data_func
        self.register_callback(app)

    def register_callback(self, app):
        category_inputs = [Input(f"{self.name}-pog-brand-id", "value")]
        app.callback(
            Output(f"{self.name}-pog-options-loader-category", "children"),
            category_inputs,
        )(self.load_categories)

        subcategory_inputs = [
            Input(f"{self.name}-pog-brand-id", "value"),
            Input(f"{self.name}-pog-dropdown-category", "value"),
        ]

        app.callback(
            Output(f"{self.name}-pog-options-loader-subcategory", "children"),
            subcategory_inputs,
        )(self.load_subcategories)

        load_option_inputs = [
            Input(f"{self.name}-pog-dropdown-subcategory", "value"),
            Input(f"{self.name}-pog-dropdown-subcategory", "options"),
            Input(f"{self.name}-include-all-checklist-input", "value"),
        ] + subcategory_inputs

        app.callback(
            Output(f"{self.name}-pog-options-panel", "children"),
            Output(f"{self.name}-pog-dropdown-subcategory", "disabled"),
            Output(f"{self.name}-pog-dropdown-subcategory", "value"),
            load_option_inputs,
        )(self.load_options)

        app.callback(
            Output(f"{self.name}-pog-dropdown-subcategory-select", "value"),
            Input(f"{self.name}-include-all-checklist-input-select", "n_clicks"),
            State(f"{self.name}-pog-dropdown-subcategory-select", "options"),
        )(self.select_all_subcats)

        app.callback(
            Output(f"{self.name}-pog-dropdown-subcategory-select", "value"),
            Input(f"{self.name}-include-all-clear-checklist-input-select", "n_clicks"),
        )(self.deselect_all_subcats)

        app.callback(
            Output(self.value_store_id, "data"),
            Input(
                {
                    "role": f"{self.name}-pog-option",
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
                    "role": f"{self.name}-pog-remove-option",
                    "option-value": ALL,
                    "option-label": ALL,
                },
                "n_clicks",
            ),
            State(self.value_store_id, "data"),
        )(self.remove_option)

        # app.callback(
        #     Output(f"{self.name}-pog-selected-options-panel", "children"),
        #     Input(self.value_store_id, "data"),
        # )(self.load_selected_options)

        app.callback(
            Output(f"{self.name}-pog-selected-options-panel", "children"),
            Output(f"{self.name}-pog-dropdown-subcategory-select", "options"),
            Input(self.value_store_id, "data"),
        )(self.load_selected_options)

        app.callback(
            Output(self.value_store_id, "data"),
            Input(f"{self.name}-pog-clear-all", "n_clicks"),
            [
                State(f"{self.name}-pog-options-panel", "children"),
                State(self.value_store_id, "data"),
            ],
        )(self.clear_selected_items)

    def clear_selected_items(self, n_clicks, children, data):
        if n_clicks:
            return None
        return dash.no_update

    def load_subcategories(self, *args):
        options = self.subcategories_data_func(*args)
        if options:
            value = None
            return dcc.Dropdown(
                id=f"{self.name}-pog-dropdown-subcategory",
                options=[{"label": x, "value": x} for x in options],
                multi=True,
                searchable=True,
                clearable=False,
                persistence=False,
                value=value,
            )
        else:
            return dcc.Dropdown(
                id=f"{self.name}-pog-dropdown-subcategory",
                options=[],
                multi=True,
                searchable=True,
                clearable=False,
                persistence=False,
            )

    def load_categories(self, *args):
        options = self.categories_data_func(*args)
        if options:
            value = None
            return dcc.Dropdown(
                id=f"{self.name}-pog-dropdown-category",
                options=[{"label": x, "value": x} for x in options],
                multi=False,
                searchable=True,
                clearable=False,
                persistence=False,
                value=value,
            )
        else:
            return dash.no_update

    def load_options(self, selected_value, all_options, include_all, *args):
        if include_all == [1]:
            selected_value = [i["value"] for i in all_options]
        if selected_value:
            options = self.options_data_func(selected_value, *args)
            options = [] if options is None else options
            descriptions = (
                self.description_data_func(selected_value, *args)
                if self.description_data_func is not None
                else None
            )
        else:
            options = []
            descriptions = []

        layout = dbc.Card(
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(
                        f"+ {options[value]}",
                        class_name="hover-list-group-item",
                        id={
                            "role": f"{self.name}-pog-option",
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
                            "role": f"{self.name}-pog-option",
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
        if include_all == [1]:
            return layout, True, None
        return layout, False, dash.no_update

    def load_selected_options(self, selected):
        if selected is not None:
            selected_subcats = POGCategory.get_subcategories_for_selected_pog(
                list(selected.keys())
            )
            if selected_subcats:
                selected_subcats_options = [
                    {"label": x, "value": x} for x in selected_subcats
                ]
            else:
                selected_subcats_options = []
            layout = dbc.Card(
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem(
                            f"- {selected[value]}",
                            class_name="hover-list-group-item",
                            id={
                                "role": f"{self.name}-pog-remove-option",
                                "option-value": value,
                                "option-label": selected[value],
                            },
                        )
                        for value in selected
                    ],
                    flush=True,
                )
            )
            return layout, selected_subcats_options
        else:
            layout = dbc.Card(
                dbc.ListGroup(
                    [],
                    flush=True,
                )
            )
            return layout, None

    # def load_selected_options(self, selected):
    #     if selected is not None:
    #         layout = dbc.Card(
    #             dbc.ListGroup(
    #                 [
    #                     dbc.ListGroupItem(
    #                         f"- {selected[value]}",
    #                         class_name="hover-list-group-item",
    #                         id={
    #                             "role": f"{self.name}-remove-option",
    #                             "option-value": value,
    #                             "option-label": selected[value],
    #                         },
    #                     )
    #                     for value in selected
    #                 ],
    #                 flush=True,
    #             )
    #         )
    #         return layout
    #     else:
    #         layout = dbc.Card(
    #             dbc.ListGroup(
    #                 [],
    #                 flush=True,
    #             )
    #         )
    #         return layout

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

    def add_all_items(self, n_clicks, children, current_selected_options):
        if n_clicks is not None:
            for item in children["props"]["children"]["props"]["children"]:
                value = item["props"]["id"]["option-value"]
                label = item["props"]["id"]["option-label"]
                current_selected_options[value] = label
            return current_selected_options
        raise PreventUpdate

    def select_all_subcats(self, nclicks, options):
        if nclicks is not None:
            return [option["value"] for option in options]
        return []

    def deselect_all_subcats(self, nclicks):
        if nclicks is not None:
            return []
        else:
            return dash.no_update
