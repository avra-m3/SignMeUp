from flask import Response
from flask_api import status


def index(*args, test: str, **kwargs):
    print(args,kwargs)
    return Response("Hello World", status.HTTP_200_OK)
