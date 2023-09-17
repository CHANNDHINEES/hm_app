from dash import html


class TrLink(html.Tr):
    def __init__(self, children, href, *args, data=None, **kwargs):
        if "style" in kwargs:
            kwargs["style"]["cursor"] = "pointer"
        else:
            kwargs["style"] = {"cursor": "pointer"}
        super().__init__(children, *args, **kwargs)
        self.href = href
        self.data = data
        self._prop_names.append("href")
        self._prop_names.append("data")
