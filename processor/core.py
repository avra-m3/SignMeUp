import json
import os
import time
from threading import Thread

import requests
from peewee import IntegrityError

from model.club import Club
from model.registration import Registration
from model.request import Request
from model.student import Student
from modules import ocr
from utilities.exception_router import APIException, Conflict


def loop():
    """
    Entry point - Handles the processing loop
    :return:
    """
    while True:
        for model in Request.select().where(Request.workflow_state == "created"):
            model.workflow_state = "processing"
            model.save()
            thread = Thread(target=process, args=[model])
            thread.start()
        time.sleep(15)


def handle_processing_errors(fn):
    """
    Wrap process with error handling to ensure the model is put in an erred
    state when an exception occurs
    :param fn: The function to wrap
    :return: the wrapped function
    :raises None: This function suppresses ALL exceptions
    """

    def wrapper(model: Request, *args, **kwargs):
        try:
            return fn(model, *args, **kwargs)
        except Exception as ex:
            print("Unexpected Exception occurred while processing")
            model.status = "failed"
            model.errors = "['{}']".join("', '".join(ex.args))
            # raise

    return wrapper


@handle_processing_errors
def process(model: Request):
    data = request_ocr(model.image_location)

    card_data = ocr.get_card_data(model.user_id, data)

    student = Student.get_or_create(id=model.user_id,
                                    first_name=card_data["first_name"],
                                    last_name=card_data["last_name"],
                                    expiry=None)
    club = Club.get_or_create(id=model.club_name)

    try:
        registration = Registration()
        registration.user_id = student.id
        registration.club_id = club.id
        registration.save()
    except IntegrityError:
        raise Conflict("A registration matching this information already exists")


def request_ocr(url: str) -> dict:
    """
    Requests OCR data from google cloud.
    This function requires an environment variable with the key 'OCR_AUTH_KEY';
    The values should be an api key with access to google's text detection api
    :return: A requests Response object
    """
    # Set Constants
    ENDPOINT = 'https://vision.googleapis.com/v1/images:annotate'
    AUTH = os.getenv('OCR_AUTH_KEY')
    HEADERS = {'Content-Type': 'application/json'}

    # Set the request structure.
    data = {
        'requests': [{
            # The image
            'image': {
                'source': {
                    'imageUri': url,
                },
            },
            # What we want in our response
            "features": [
                {
                    "type": "TEXT_DETECTION"
                }
            ],
            # Make processing more accurate by specifying english as the language
            "imageContext": {
                "languageHints": [
                    "en"
                ]
            }
        }]
    }
    # Make POST request and return the response.
    response = requests.post(ENDPOINT,
                             data=json.dumps(data),
                             params={'key': AUTH},
                             headers=HEADERS
                             )

    if response.status_code != 200:
        raise APIException("Upstream gateway returned an unacceptable response", status=502)

    return response.json()
