# from asyncio.windows_events import NULL
import dash_bootstrap_components as dbc
import numpy as np
from dash import html
import pandas as pd
from components.component_helpers import (
    create_decision_dropdown,
    create_comment_input,
    create_comment_input_batch,
    create_comment_input_batch_wo_tooltip,
    create_check_box,
    create_comment_input_button_batch_wo_tooltip,
)


def initial_row_cell_value(delete_role, edit_role, result):
    """
    Initial cell for each row in add product batch
    TODO: This should really be a class
    TODO: Consolidate initial_row_cell_value_batch and initial_row_cell_value

    Args:
        delete_role (str): identifier for the delete button, None if delete is disabled
        edit_role (str): identifier for the edit/update button, None if update is disabled
        result: row data
    """
    cells = []
    if delete_role is None and edit_role is None:
        cells = []
    elif delete_role is None:
        cells = [
            html.Td(
                [
                    dbc.Button(
                        "Edit ",
                        color="primary",
                        outline=True,
                        size="sm",
                        id={"role": edit_role, "p_key": result["p_key"]},
                    )
                ],
                className="d-grid gap-2",
            )
        ]
    elif edit_role is None:
        cells = [
            html.Td(
                [
                    dbc.Button(
                        "Delete ",
                        color="danger",
                        outline=True,
                        size="sm",
                        id={"role": delete_role, "p_key": result["p_key"]},
                    )
                ],
                className="d-grid gap-2",
            )
        ]
    else:
        cells = [
            html.Td(
                [
                    dbc.Button(
                        "Delete",
                        color="danger",
                        outline=True,
                        size="sm",
                        id={"role": delete_role, "p_key": result["p_key"]},
                    ),
                    dbc.Button(
                        "Update",
                        color="primary",
                        outline=True,
                        size="sm",
                        id={"role": edit_role, "p_key": result["p_key"]},
                    ),
                ],
                className="d-grid gap-2 d-md-flex justify-content-md-end",
            )
        ]
    return cells


def create_table_row(result, column_names, delete_role, edit_role, format_dict):
    """
    A custom data table row that has editable cells and read only cells for adding npd in batch
    TODO: This should really be a class
    TODO: Consolidate create_data_table_batch and create_data_table

    Args:
        format_dict: format dictionary
        result: The table row to render
        column_names : names of column
        delete_role (str): identifier for the delete button, None if delete is disabled
        edit_role (str): identifier for the edit/update button, None if update is disabled
    """
    cells = initial_row_cell_value(delete_role, edit_role, result)
    # Create a cell for each column
    for col in column_names:
        # Special columns Decision and Comment are editable
        if col == "Decision":
            cells.append(
                html.Td(
                    create_decision_dropdown(value=result[col], p_key=result["p_key"]),
                    style={"padding": "3px", "minWidth": "250px", "textAlign": "left"},
                )
            )
        elif col == "Comment":
            cells.append(
                html.Td(
                    create_comment_input(
                        value=result[col] if result[col] is not None else "",
                        p_key=result["p_key"],
                    ),
                    style={"padding": "3px", "minWidth": "250px", "textAlign": "left"},
                )
            )
        # All other columns are read only
        else:
            if isinstance(result[col], np.ndarray) or isinstance(result[col], list):
                temp = [str(i) for i in result[col]]
                text = ", ".join(temp)
                cells.append(html.Td(text, style={"padding": "3px"}))
            else:
                if col in format_dict.keys():
                    if (
                        format_dict[col] == "dollar"
                        or format_dict[col] == "percent"
                        or format_dict[col] == "decimal"
                    ):
                        text = result[col]
                        cells.append(
                            html.Td(
                                text, style={"padding": "3px", "textAlign": "right"}
                            )
                        )
                    elif format_dict[col] == "string" or format_dict[col] == "date":
                        if result[col] is not None and pd.isna(result[col]) != True:
                            text = result[col].strip('"')
                            cells.append(
                                html.Td(
                                    text, style={"padding": "3px", "textAlign": "left"}
                                )
                            )
                        else:
                            text = result[col]
                            cells.append(html.Td(text, style={"padding": "3px"}))
                    else:
                        text = result[col]
                        cells.append(html.Td(text, style={"padding": "3px"}))
    return html.Tr(cells, id=f"table-row-{result['p_key']}")


def create_data_table(results, column_format_df, delete_role=None, edit_role=None):
    """
    A custom data table that has editable cells and read only cells
    TODO: This should really be a class

    Args:

        column_format_df:
        results (pandas.Dataframe): The table to render
        delete_role (str): identifier for the delete button, None if delete is disabled
        edit_role (str): identifier for the update/edit button, None if delete is disabled:
    """
    # Add on a delete column if there is a delete function
    column_names = (
        results.columns if delete_role is None else [""] + list(results.columns)
    )

    # Make the table header stick to the top
    table_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th(
                        col,
                        style={
                            "zIndex": "1",
                            "position": "sticky",
                            "top": "-1px",
                            "background": "white",
                            "bottomBorder": "1px solid var(--bs-gray-300)",
                            "fontWeight": "bold",
                            "fontSize": "16px",
                            "fontFamily": "Arial, Helvetica, sans-serif",
                        },
                    )
                    for col in column_names
                    if col != "p_key"
                ]
            )
        )
    ]

    column_names = [col for col in results.columns if col != "p_key"]
    column_format_df1 = column_format_df[
        column_format_df["Display Name"].isin(column_names)
    ]
    format_dict = dict()
    type_dict = dict()
    for index, result in column_format_df1.iterrows():
        if result["Format"] == "dollar":
            precision_format = (
                "${:." + str(result["Precision"]).strip().split(".")[0] + "f}"
            )
            type_dict[result["Display Name"]] = result["Format"]
            format_dict[result["Display Name"]] = precision_format
        elif result["Format"] == "percent":
            precision_format = (
                "{:." + str(result["Precision"]).strip().split(".")[0] + "%}"
            )
            format_dict[result["Display Name"]] = precision_format
            type_dict[result["Display Name"]] = result["Format"]
        elif result["Format"] == "decimal":
            precision_format = (
                "{:." + str(result["Precision"]).strip().split(".")[0] + "f}"
            )
            format_dict[result["Display Name"]] = precision_format
            type_dict[result["Display Name"]] = result["Format"]
        else:
            format_dict[result["Display Name"]] = "No Format"
            type_dict[result["Display Name"]] = result["Format"]

    for key, value in format_dict.items():
        if value != "No Format":
            results[key].fillna(0, inplace=True)
            results[key] = results[key].apply(value.format)

    # Generate the rows
    children = []
    for index, result in results.iterrows():
        # Add the cells to a HTML Row
        children.append(
            create_table_row(
                result=result,
                delete_role=delete_role,
                edit_role=edit_role,
                column_names=column_names,
                format_dict=type_dict,
            )
        )
    # Create the table body
    table_body = [html.Tbody(children)]

    # Finalise the table as a dash_bootstrap_components  table
    table = dbc.Table(table_header + table_body, hover=True, bordered=True)

    return table


##########################################################################
# Data table helper functions specific to add product batch
def create_data_table_batch(
    results,
    column_format_df,
    delete_role=None,
    validate_role=None,
):
    """
    A custom data table that has editable cells and read only cells for adding npd in batch
    TODO: This should really be a class
    TODO: Consolidate create_data_table_batch and create_data_table

    Args:
        validate_role: identifier for the delete button, None if delete is disabled
        column_format_df: format df
        results (pandas.Dataframe): The table to render
        delete_role (str): identifier for the delete button, None if delete is disabled
    """
    # Add on a delete column if there is a delete function
    column_names = (
        results.columns if delete_role is None else [""] + list(results.columns)
    )

    # Make the table header stick to the top
    table_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th(
                        col,
                        style={
                            "zIndex": "1",
                            "position": "sticky",
                            "top": "-1px",
                            "background": "white",
                            "bottomBorder": "1px solid var(--bs-gray-300)",
                            "fontWeight": "bold",
                            "fontSize": "16px",
                            "fontFamily": "Arial, Helvetica, sans-serif",
                            "padding": "1rem",
                        },
                    )
                    for col in column_names
                    if col not in ["p_key", "DistributionPercentage", "Distribution %"]
                ]
            )
        )
    ]

    column_names = [
        col
        for col in results.columns
        if col not in ["p_key", "DistributionPercentage", "Distribution %"]
    ]
    column_format_df1 = column_format_df[
        column_format_df["Display Name"].isin(column_names)
    ]
    format_dict = dict()
    type_dict = dict()
    for index, result in column_format_df1.iterrows():
        if result["Format"] == "dollar":
            precision_format = (
                "{:." + str(result["Precision"]).strip().split(".")[0] + "f}"
            )
            type_dict[result["Display Name"]] = result["Format"]
            format_dict[result["Display Name"]] = precision_format
        elif result["Format"] == "percent":
            precision_format = (
                "{:." + str(result["Precision"]).strip().split(".")[0] + "%}"
            )
            format_dict[result["Display Name"]] = precision_format
            type_dict[result["Display Name"]] = result["Format"]
        elif result["Format"] == "decimal":
            precision_format = (
                "{:." + str(result["Precision"]).strip().split(".")[0] + "f}"
            )
            format_dict[result["Display Name"]] = precision_format
            type_dict[result["Display Name"]] = result["Format"]
        else:
            format_dict[result["Display Name"]] = "No Format"
            type_dict[result["Display Name"]] = result["Format"]

    for key, value in format_dict.items():
        if value != "No Format":
            results[key].fillna(0, inplace=True)
            results[key] = results[key].apply(value.format)

    # Generate the rows
    children = []
    for index, result in results.iterrows():
        # Add the cells to a HTML Row
        children.append(
            create_table_row_batch(
                result=result,
                delete_role=delete_role,
                validate_role=validate_role,
                column_names=column_names,
            )
        )
    # Create the table body
    table_body = [html.Tbody(children)]

    # Finalise the table as a dash_bootstrap_components  table
    table = dbc.Table(table_header + table_body, hover=True, bordered=True)
    return table


def create_table_row_batch(result, column_names, delete_role, validate_role):
    """
    Creating a table row
    TODO: This should really be a class
    TODO: Consolidate initial_row_cell_value_batch and initial_row_cell_value

    Args:
        validate_role: identifier for the validate button, None if validate is disabled
        column_names: column names
        delete_role (str): identifier for the delete button, None if delete is disabled
        result: row data
    """
    cells = initial_row_cell_value_batch(delete_role, validate_role, result)
    # Create a cell for each column
    for col in column_names:
        if col in ["Validation status"]:
            cells.append(
                html.Td(
                    create_comment_input_batch_wo_tooltip(
                        value=result[col] if result[col] is not None else "",
                        p_key=result["p_key"],
                        disabled=True,
                        columnname=col,
                    ),
                    style={
                        "width": "100%",
                        "padding": "3px",
                        "minWidth": "250px",
                        "textAlign": "centre",
                        "justify-content": "center",
                    },
                )
            )
        elif col in [
            "Distribution_percentage",
            "DistributionPercentage",
            "Distribution %",
        ]:
            pass
        elif col in ["Replaces existing NPD"]:
            if result[col] == "Yes":
                cells.append(
                    html.Td(
                        create_comment_input_batch_wo_tooltip(
                            value=result[col] if result[col] is not None else "",
                            p_key=result["p_key"],
                            disabled=True,
                            columnname=col,
                            font_color="red",
                        ),
                        style={
                            "width": "100%",
                            "padding": "3px",
                            "minWidth": "250px",
                            "textAlign": "centre",
                            "justify-content": "center",
                        },
                    )
                )
            else:
                cells.append(
                    html.Td(
                        create_comment_input_batch_wo_tooltip(
                            value=result[col] if result[col] is not None else "",
                            p_key=result["p_key"],
                            disabled=True,
                            columnname=col,
                            font_color="gray",
                        ),
                        style={
                            "width": "100%",
                            "padding": "3px",
                            "minWidth": "250px",
                            "textAlign": "centre",
                            "justify-content": "center",
                        },
                    )
                )
        elif col in ["Validation error"]:
            cells.append(
                html.Td(
                    create_comment_input_batch(
                        value=result[col] if result[col] is not None else "",
                        p_key=result["p_key"],
                        disabled=True,
                        columnname=col,
                    ),
                    style={
                        "width": "100%",
                        "padding": "3px",
                        "minWidth": "250px",
                        "textAlign": "centre",
                        "justify-content": "center",
                    },
                )
            )
        elif col in ["POG Category", "Cluster"]:
            cells.append(
                html.Td(
                    create_comment_input_button_batch_wo_tooltip(
                        value=result[col] if result[col] is not None else "",
                        p_key=result["p_key"],
                        columnname=col,
                    ),
                    style={
                        "width": "100%",
                        "padding": "3px",
                        "minWidth": "250px",
                        "textAlign": "centre",
                        "justify-content": "center",
                    },
                )
            )
        else:
            cells.append(
                html.Td(
                    create_comment_input_batch_wo_tooltip(
                        value=result[col] if result[col] is not None else "",
                        p_key=result["p_key"],
                        columnname=col,
                        font_color="gray",
                    ),
                    style={
                        "width": "100%",
                        "padding": "3px",
                        "minWidth": "250px",
                        "textAlign": "centre",
                        "justify-content": "center",
                    },
                )
            )
    # return html.Tr(cells, id=f"batch-table-row-{result['p_key']}")
    return html.Tr(cells, id={"role": "batch-table-row", "p_key": result["p_key"]})


def initial_row_cell_value_batch(delete_role, validate_role, result):
    """
    Initial cell for each row in add product batch
    TODO: This should really be a class
    TODO: Consolidate initial_row_cell_value_batch and initial_row_cell_value

    Args:
        delete_role (str): identifier for the delete button, None if delete is disabled
        validate_role (str): identifier for the validate button, None if validate is disabled
        result: row data
    """
    cells = []
    if delete_role is None and validate_role is None:
        cells = []
    elif delete_role is None:
        cells = [
            html.Td(
                [
                    dbc.Button(
                        "Validate",
                        color="primary",
                        outline=True,
                        size="sm",
                        id={
                            "role": "batch_import_" + validate_role,
                            "p_key": result["p_key"],
                        },
                        style={"font-size": "10px", "padding": "1mm 1mm"},
                    )
                ],
                className="d-grid gap-2",
                style={"padding": "1mm 1mm"},
                id={"role": "batch_button_place_holder", "p_key": result["p_key"]},
            )
        ]
    elif validate_role is None:
        cells = [
            html.Td(
                [
                    dbc.Button(
                        "Delete",
                        color="danger",
                        outline=True,
                        size="sm",
                        id={
                            "role": "batch_import_" + delete_role,
                            "p_key": result["p_key"],
                        },
                        style={"font-size": "10px", "padding": "1mm 1mm"},
                    )
                ],
                className="d-grid gap-2",
                style={"padding": "1mm 1mm"},
                id={"role": "batch_button_place_holder", "p_key": result["p_key"]},
            )
        ]
    else:
        cells = [
            html.Td(
                [
                    create_check_box(result["p_key"]),
                ],
                className="d-grid gap-2 d-md-flex justify-content-md-end",
                style={"padding": "1mm 1mm"},
                id={"role": "batch_button_place_holder", "p_key": result["p_key"]},
            )
        ]

    return cells
