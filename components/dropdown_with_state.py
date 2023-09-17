from dash import dcc


class DropdownWithState(dcc.Dropdown):
    def __init__(self, className, *args, data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data
        self.className = className
        self.available_properties.append("data")
        self._prop_names.append("data")
