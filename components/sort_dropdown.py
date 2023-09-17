import dash_bootstrap_components as dbc
from dash import html, dcc


def create_sort_dropdown(options):
    return dcc.Dropdown(
        id="sort-dropdown-id",
        placeholder="Sort By",
        options=options,
        multi=False,
        persistence=True,
        persistence_type="session",
    )


sort_dropdown = dbc.Row(
    [
        dbc.Col(
            html.Table(
                html.Tr(
                    [
                        html.Td(
                            "Sort by:",
                            style={
                                "paddingLeft": "10px",
                                "width": "30px",
                                "whiteSpace": "nowrap",
                                "paddingRight": "10px",
                            },
                        ),
                        html.Td(
                            create_sort_dropdown([]),
                            style={"width": "200px"},
                            id="sort-cell-id",
                        ),
                    ]
                )
            )
        )
    ],
    align="center",
    style={"height": "100%", "marginRight": "10px"},
)
