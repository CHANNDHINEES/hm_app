import dash_bootstrap_components as dbc
from dash import dcc
from components.dropdown_with_state import DropdownWithState
from components.smart_badge import SmartBadge
from utils.constants import DECISION_OPTIONS
from dash import html


def create_filter_tag(column, text, include, index):
    includeFilter = "IS"
    if not include:
        includeFilter = "IS NOT"
    return SmartBadge(
        f"{column}: {includeFilter} {text} [X]",
        data={"column": column, "phrase": text, "include": include},
        color="info",
        className="me-1",
        style={"cursor": "pointer"},
        id={"role": "filter", "index": index},
    )


def create_decision_dropdown(value, p_key):
    options = DECISION_OPTIONS
    return DropdownWithState(
        id={"role": "decision-dropdown-id", "p_key": p_key, "prev_value": value},
        className="decision-dropdown-id",
        options=[{"label": x, "value": x} for x in options],
        multi=False,
        searchable=False,
        clearable=False,
        persistence=False,
        value=value,
        data=value,
    )


def create_comment_input(value, p_key):
    return dcc.Input(
        id={"role": "comment-input-id", "p_key": p_key, "prev_value": value},
        className="comment-input-id",
        value=value,
        style={"height": "36px", "width": "100%"},
    )


def create_comment_input_batch(
    value, p_key, columnname, font_color="gray", disabled=False
):
    return html.Div(
        [
            dcc.Input(
                id={"role": f"batch-{columnname}-id", "p_key": p_key},
                className="batch-comment-input-id",
                value=value,
                disabled=disabled,
                debounce=True,
                style={
                    "height": "40px",
                    "width": "100%",
                    "overflow-x": "auto",
                    "color": font_color,
                },
            ),
            dbc.Tooltip(
                value,
                target={"role": f"div_batch-{columnname}-id", "p_key": p_key},
                id={"role": f"tooltip_batch-{columnname}-id", "p_key": p_key},
                placement="top",
            ),
        ],
        id={"role": f"div_batch-{columnname}-id", "p_key": p_key},
    )


def create_comment_input_batch_wo_tooltip(
    value, p_key, columnname, font_color="gray", disabled=False
):
    return html.Div(
        [
            dcc.Input(
                id={"role": f"batch-{columnname}-id", "p_key": p_key},
                className="batch-comment-input-id",
                value=value,
                disabled=disabled,
                debounce=True,
                style={
                    "height": "40px",
                    "width": "100%",
                    "overflow-x": "auto",
                    "color": font_color,
                },
            )
        ],
        id={"role": f"div_batch-{columnname}-id", "p_key": p_key},
    )


def create_check_box(p_key):
    return html.Div(
        [
            dcc.Checklist(
                id={"role": f"batch-checkbox-id", "p_key": p_key},
                className="batch-comment-input-id",
                value=[p_key],
                options=[{"label": "", "value": p_key}],
                style={"padding": "1mm"},
            )
        ],
        id={"role": f"div_batch-checkbox-id", "p_key": p_key},
    )


def create_comment_input_button_batch_wo_tooltip(
    value, p_key, columnname, font_color="gray", disabled=False
):
    modal_content = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("SELECT")),
            dbc.ModalBody(
                [
                    dbc.Form(
                        [
                            dbc.Spinner(
                                html.Div(
                                    id={
                                        "role": f"batch-{columnname}-panel-id",
                                        "p_key": p_key,
                                    },
                                    style={"minHeight": "200px"},
                                )
                            ),
                        ],
                    )
                ]
            ),
            dbc.ModalFooter(
                html.Div(
                    [
                        dbc.Button(
                            "Select",
                            id={
                                "role": f"batch-{columnname}-select-button-id",
                                "p_key": p_key,
                            },
                            className="me-1",
                            n_clicks=0,
                        )
                    ]
                )
            ),
        ],
        id={"role": f"batch-{columnname}-modal", "p_key": p_key},
        is_open=False,
        size="xl",
        scrollable=True,
    )

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Input(
                            id={"role": f"batch-{columnname}-id", "p_key": p_key},
                            className="batch-comment-input-id",
                            value=value,
                            disabled=disabled,
                            debounce=True,
                            style={
                                "height": "40px",
                                "width": "210px",
                                "overflow-x": "auto",
                                "color": font_color,
                            },
                        )
                    ),
                    dbc.Col(
                        dbc.Button(
                            "🠑",
                            size="sm",
                            id={
                                "role": f"batch-{columnname}-button-id",
                                "p_key": p_key,
                            },
                            style={"width": "15px", "font-size": "18px"},
                        )
                    ),
                ],
                className="g-0",
            ),
            modal_content,
        ]
    )
