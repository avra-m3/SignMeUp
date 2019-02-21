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

    def handler(self) -> Response:
        """
        Handle an APIException and transform it into response
        :param self: The Api Exception object
        :return: A JSON werkzuig response object
        """
        result = {
            "code": self.status,
            "status": self.status_message,
            "message": self.detail,
        }
        if self.payload is not None:
            result["data"] = self.payload
        print(result)
        response = jsonify(result)
        response.status_code = self.status
        return response


class BadRequest(APIException):
    _status = 400
    _detail = "Bad Request"


class NotAcceptable(APIException):
    _status = 406
    _detail = "Not Acceptable"


class PreconditionFailed(APIException):
    """
    Note: This exception will return an empty response
    For more information see: https://github.com/pallets/werkzeug/issues/1231

    Solution:
    Upgrade to v0.15 on release where https://github.com/pallets/werkzeug/pull/1255 will hopefully be in effect.
    """
    _status = 412
    _detail = "Precondition Failed"

    def handler(self) -> Response:
        """
        <b>HACK</b>
        Override the default behaviour and have a 412 be sent with 400 (next closest status code) so the message is
        sent to the end user.
        :return:
        """
        result = APIException.handler(self)
        result.status_code = 400
        return result


class Conflict(APIException):
    _status = 409
    _detail = "Conflict"


class NotFound(APIException):
    _status = 404
    _detail = "Not Found"


class Unauthorized(APIException):
    _status = 401
    _detail = "Unauthorized"


class Forbidden(APIException):
    _status = 403
    _detail = "Forbidden"
