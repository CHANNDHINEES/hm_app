import dash_bootstrap_components as dbc
from dash import html, dcc
import dash_daq as daq


def create_filter_dropdown(options):
    return dcc.Dropdown(
        id="filter-dropdown-id",
        placeholder="Filter",
        options=options,
        multi=False,
        persistence=True,
        persistence_type="session",
    )


filter_control = dbc.Row(
    [
        dbc.Col(
            html.Table(
                html.Tr(
                    [
                        html.Td(
                            "Add Filter:",
                            style={"width": "80px", "whiteSpace": "nowrap"},
                        ),
                        html.Td(
                            create_filter_dropdown([]),
                            style={"width": "400px"},
                            id="filter-cell-id",
                        ),
                        html.Td(
                            dbc.Input(
                                placeholder="Search Phrase",
                                id="filter-phrase",
                                style={"borderRadius": "5%", "borderWidth": "2px"},
                            ),
                            style={
                                "width": "400px",
                                "paddingLeft": "10px",
                                "paddingRight": "10px",
                            },
                        ),
                        html.Td(
                            daq.BooleanSwitch(
                                id="include-toggle",
                                label="Include",
                                labelPosition="bottom",
                                on=True,
                            )
                        ),
                        html.Td(
                            dbc.Button("Add", id="add-filter-button"),
                            style={"paddingLeft": "20px", "paddingRight": "10px"},
                        ),
                        html.Td(
                            [
                                html.Span(
                                    "Filters",
                                    style={
                                        "marginLeft": "20px",
                                        "position": "absolute",
                                        "fontSize": "10px",
                                        "color": "gray",
                                    },
                                ),
                                html.Div(
                                    [],
                                    id="filters-panel",
                                    style={
                                        "overflowY": "scroll",
                                        "overflowX": "auto",
                                        "height": "60px",
                                        "padding": "10px",
                                        "whiteSpace": "nowrap",
                                        "width": "300px",
                                        "border": "1px gray solid",
                                        "borderRadius": "5px",
                                    },
                                ),
                            ]
                        ),
                    ]
                )
            ),
            width=10,
        )
    ],
    align="center",
    style={"height": "100%"},
)
