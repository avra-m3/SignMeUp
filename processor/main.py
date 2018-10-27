import json
import os
import re
import time
from base64 import b64encode
from threading import Thread

import requests
from peewee import IntegrityError

from model.student import Student
from model.club import Club
from model.registration import Registration
from model.request import Request
from modules.ocr.process import get_card_data
from utilities.exception_router import APIException


def loop():
    while True:
        for model in Request.select().where(Request.workflow_state == "created"):
            model.workflow_state = "processing"
            model.save()
            thread = Thread(target=process, args=[model])
            thread.start()
        time.sleep(30)


def handle_processing_errors(fn):
    def wrapper(model: Request, *args, **kwargs):
        try:
            return fn(model, *args, **kwargs)
        except Exception as ex:
            print("Unexpected Exception occurred while processing")
            model.status = "failed"
            model.errors = "['{}']".join("', '".join(ex.args))
            # Todo: Remove in prod
            # raise

    return wrapper


@handle_processing_errors
def process(model: Request):
    response = request_ocr(model.image_location)
    if response.status_code != 200:
        raise APIException("Upstream gateway returned an unacceptable response", status=504)

    data = response.json()
    user_id = re.match("21259(\d{7})\d{2}", model.card_number).groups()[0]

    card_data = get_card_data(user_id, data)

    try:
        card = Student(card_id=user_id)
        card.first_name = card_data["first_name"]
        card.last_name = card_data["last_name"]
        card.expiry = None
        card.save()
    except IntegrityError:
        pass


    club = Club.get_or_create(id=model.club_name)

    try:
        registration = Registration()
        registration.user_id = model.card_number
        registration.club_id = model.club_name
        registration.year = model.reg_year
        registration.save()
    except IntegrityError:
        raise


def request_ocr(path: str) -> requests.Response:
    """
    Requests OCR data from google cloud.
    This function requires an environment variable with the key 'OCR_AUTH_KEY';
    The values should be an api key with access to google's text detection api
    :param path: The path to file
    :return: A requests Response object
    """
    # Set Constants
    ENDPOINT = 'https://vision.googleapis.com/v1/images:annotate'
    AUTH = os.getenv('OCR_AUTH_KEY')
    HEADERS = {'Content-Type': 'application/json'}

    # Open the image as a binary file
    with open(path, "rb") as image:
        contents = image.read()

        # Encode the image as base 64; convert it to unicode for the request.
        image_contents = b64encode(contents).decode()

        # Set the request structure.
        data = {
            'requests': [{
                # The image
                'image': {'content': image_contents},
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
        return requests.post(ENDPOINT,
                             data=json.dumps(data),
                             params={'key': AUTH},
                             headers=HEADERS
                             )
