import json


class ProcessingException(Exception):
    _exc = "Processing Failed"

    detail: str
    exc: str

    def __init__(self, detail="", exc=None):
        self.exc = self._exc
        self.detail = detail

        if exc is not None:
            self.exc = exc

    @property
    def json(self) -> str:
        return json.dumps({
            "status": "failed",
            "error": self.exc,
            "message": self.detail
        })


class BoundError(ProcessingException):
    _exc = "Bound Set Invalid"


class FieldError(ProcessingException):
    _exc = "Field Not Found"


class ConflictError(ProcessingException):
    _exc = "Duplicate Fields Found"


class UpstreamError(ProcessingException):
    _exc = "Upstream API Failed"
