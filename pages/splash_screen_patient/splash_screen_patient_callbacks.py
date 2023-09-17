# from dash import Input, Output
# from utils.functions import get_username
# from app import app
#
#
# @app.callback(Output("username", "children"), Input("username", "children"))
# def username_display(children):
#     """Gets the username from the request headers and displays on the page"""
#     try:
#         return f"Welcome {get_username()}"
#     except KeyError:
#         return "Welcome Anonymous"
