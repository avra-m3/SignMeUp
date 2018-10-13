import http

from flask import Response, jsonify


class APIException(Exception):
    _status = 500
    _detail = "Internal Server Error"
    _payload = None

    status: str
    detail: str
    payload: dict

    def __init__(self, detail=None, status=None, payload=None):
        """
        Api exception constructor
        :param detail: The reason this exception was thrown, defaults to _detail
        :param status: The HTTP status of the exception thrown, defaults to _status
        :param payload: The data associated with the thrown exception, defaults to _payload
        """
        if status is None:
            status = self._status
        if detail is None:
            detail = self._detail
        if payload is None:
            payload = self._payload
        Exception.__init__(self)
        self.detail = detail
        self.status = status
        self.payload = payload

    @property
    def status_message(self) -> str:
        try:
            return "HTTP {} {}".format(self.status, http.HTTPStatus(self.status).phrase)
        except ValueError:
            return "HTTP {}".format(self.status)

    @staticmethod
    def handler(exc) -> Response:
        """
        Handle an APIException and transform it into response
        :param exc: The Api Exception object
        :return: A JSON werkzuig response object
        """
        result = {
            "code": exc.status,
            "status": exc.status_message,
            "message": exc.detail,
        }
        if exc.payload is not None:
            result["data"] = exc.payload
        response = jsonify(result)
        response.status_code = exc.status
        return response


class BadRequest(APIException):
    _status = 400
    _detail = "Bad Request"


class NotAcceptable(APIException):
    _status = 406
    _detail = "Not Acceptable"


class PreconditionFailed(APIException):
    _status = 412
    _detail = "Precondition Failed"

class Conflict(APIException):
    _status = 409
    _detail = "Conflict"
