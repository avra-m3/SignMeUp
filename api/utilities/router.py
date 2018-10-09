from typing import List, Tuple, Optional

from flask import Flask, request

from utilities.exception_router import ParseError, APIException


class Route:
    url: str
    methods: List[str]
    _call: staticmethod
    params: Tuple[str, type, Optional[bool]]

    def __init__(self, url: str, methods: List[str], call: staticmethod):
        self.url = url
        self.methods = methods
        self.call = call
        self._has_form = False
        self._has_json = False

    @property
    def call(self) -> staticmethod:
        """
        Previously wrapped exception handling here
        :return: static method
        """
        return self._call

    @call.setter
    def call(self, value):
        self._call = value

    def has_query_params(self, *params: Tuple[str, type, Optional[bool]]):
        """
        This function will insert the matching query parameter as a function argument when the route is called.
        :param params: A tuple containing the string parameter name, the type of parameter, and whether or not this
        param is optional (if true, the parameter will be set to 'None' when it does not exist and still passed).
        :return: self
        """
        func = self._call

        def wrapper(*args, **kwargs):
            context = dict([(c[0], [c[1], c[2]]) for c in params])
            for param in request.args:
                if param in context.keys():
                    try:
                        value = context[param][0](request.args[param])
                        kwargs[param] = value
                        context.pop(param)
                    except Exception:
                        errstr = "Request param {} was not the expected type ({})".format(param,
                                                                                          context[param][0].__str__())
                        raise ParseError(errstr)
            for key in context:
                if context[key][1]:
                    kwargs[key] = None
                else:
                    missing_args = ",".join([key for key in context if not context[key][1]])
                    errstr = "The following parameters were missing from the request url: {}".format(missing_args)
                    raise ParseError(errstr)
            return func(*args, **kwargs)

        self.call = wrapper
        return self

    def has_args(self, *values: Tuple[str, Optional[type], Optional[bool]]):
        """
        Declare this route has a set of required arguments and pass them into function params.
        :param values: A tuple containing the string arg name, the type of arg, and whether or not this
        arg is optional(if true, the parameter will be set to 'None' when it does not exist and still passed).
        :return: self
        """
        # Attempt json, fall back to form data
        data = request.json

        if not data:
            data = request.values

        func = self._call

        def wrapper(*args, **kwargs):
            context = dict([(c[0], [len(c) > 1 and c[1] or None, len(c) > 2 and c[2] or False]) for c in values])
            for argument in data:
                if argument in context.keys():
                    try:
                        value = data[argument]
                        if context[argument][0] is not None:
                            value = context[argument][0](data[argument])
                        kwargs[argument] = value
                        context.pop(argument)
                    except ValueError:
                        errstr = "Request param {} was not the expected type ({})".format(argument,
                                                                                          context[argument][
                                                                                              0].__str__())
                        raise ParseError(errstr)
            for key in context:
                if context[key][1]:
                    kwargs[key] = None
                else:
                    missing_args = ",".join([key for key in context if not context[key][1]])
                    errstr = "The following arguments were missing from the request body: {}".format(missing_args)
                    raise ParseError(errstr)
            return func(*args, **kwargs)

        self.call = wrapper
        return self


def create_routes(app: Flask, urls: List[Route]) -> None:
    """
    This function generates the flask routes based on the list above
    :param app: The flask application context
    :param urls: A list of lists
    :return: None
    """
    app.errorhandler(APIException)(APIException.handler)
    for route in urls:
        app.route(route.url, methods=route.methods)(route.call)
