"""ParsedURL Helper Class"""


class ParsedUrl:
    """Parse URL Parameters"""

    base_url: str
    params: dict[str, str]
    raw_url: str

    def __init__(self, url: str):
        self.raw_url = url
        self.base_url, params_url = url.split("?")
        params_list = params_url.split("&")
        self.params = {}
        for i in params_list:
            p, v = i.split("=")
            try:
                self.params[p] = int(v)
            except ValueError:
                self.params[p] = v

    def __str__(self) -> str:
        return f"ParsedUrl(base_url='{self.base_url}', params={self.params})"
