import dash_bootstrap_components as dbc
from dash import dcc, Output, Input, State, html, no_update
from datetime import date


class DownloadDFMenuItem(dbc.DropdownMenuItem):
    def __init__(
        self,
        children,
        id,
        app,
        dataframe_function,
        alert_panel_id,
        file_type="csv",
        alert_duration=4000,
        alert_text=None,
        filename=None,
        state_inputs=None,
        index=False,
        **kwargs,
    ):
        if not isinstance(children, list):
            children = [children]
        children.append(dcc.Download(id=f"{id}-download"))

        super().__init__(children, id, **kwargs)

        alert_text = alert_text if alert_text is not None else "Preparing download."
        filename = filename if filename is not None else f"download.{file_type}"

        self.alert_panel_id = alert_panel_id
        self.alert_duration = alert_duration
        self.alert_text = alert_text
        self.file_type = file_type
        self.dataframe_function = dataframe_function
        self.state_inputs = state_inputs
        self.index = index
        self.filename = filename
        self.register_callback(app)

    def register_callback(self, app):
        # Callback for the initial click which displays the alert and activates the df processing async
        # Interval is used so the UI is updated with the alert before the longer running process_df function runs
        app.callback(
            Output(self.alert_panel_id, "children"),
            Input(self.id, "n_clicks"),
            prevent_initial_call=True,
        )(self.__on_click)

        # When the async interval triggers start generating file for download.
        outputs = Output(f"{self.id}-download", "data")
        # inputs = Input(f'{self.id}-alert', 'n_intervals')
        inputs = [
            State("review-name", "data"),
            Input(f"{self.id}-alert", "n_intervals"),
        ]

        if self.state_inputs is not None:
            app.callback(outputs, inputs, self.state_inputs)(self.__process_df)
        else:
            app.callback(outputs, inputs)(self.__process_df)

    def __on_click(self, n_clicks):
        children = [
            dbc.Alert(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Span(
                                        self.alert_text, style={"paddingRight": "30px"}
                                    ),
                                    dbc.Spinner(size="sm"),
                                ],
                                width={"size": 4, "offset": 4},
                                style={"textAlign": "center"},
                            )
                        ]
                    )
                ],
                is_open=True,
                duration=self.alert_duration,
            ),
            dcc.Interval(interval=100, max_intervals=1, id=f"{self.id}-alert"),
        ]
        return children

    @staticmethod
    def get_filename(id, review_name, file_type):
        if id == "export-review-data-menu-item":
            return f'ReviewData_{review_name}_{date.today().strftime("%d-%m-%Y")}.{file_type}'

        if id == "export-new-products-menu-item":
            return f'NewProducts_{review_name}_{date.today().strftime("%d-%m-%Y")}.{file_type}'

        if id == "export-assortment-menu-item":
            return f'Assortment_{review_name}_{date.today().strftime("%d-%m-%Y")}.{file_type}'

    def __process_df(self, n, review_name, *args):
        df = self.dataframe_function(*args)
        if self.file_type == "xlsx":
            file_name = self.get_filename(self.id, review_name, self.file_type)
            return dcc.send_data_frame(
                df.to_excel, file_name, sheet_name="Sheet 1", index=self.index
            )
        elif self.file_type == "csv":
            file_name = self.get_filename(self.id, review_name, self.file_type)
            return dcc.send_data_frame(df.to_csv, file_name, index=self.index)
