

class notFoundException(Exception):
    def __init__(self, detail: str|None = None):
        self.detail = "Entry not found"
        self.moreDetail = detail

class httpxException(Exception):
    def __init__(self, detail: str|None = None):
        self.detail = "Connection to Internal failed"
        self.moreDetail = detail