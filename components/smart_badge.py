import dash_bootstrap_components as dbc


class SmartBadge(dbc.Badge):
    def __init__(self, children, data, *args, **kwargs):
        super().__init__(children, *args, **kwargs)
        self.data = data
        self._prop_names.append("data")
