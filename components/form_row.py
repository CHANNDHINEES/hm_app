import dash_bootstrap_components as dbc


class FormRow(dbc.Row):
    def __init__(
        self,
        name,
        text,
        control,
        html_for="",
        label_width=3,
        control_width=5,
        offset=2,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.children = [
            dbc.Col(
                dbc.Label(text, html_for=html_for),
                width={"size": label_width, "offset": offset},
            ),
            dbc.Col(control, width=control_width),
        ]
        self.className = ("mb-3",)
        self.id = f"{name}-id"
