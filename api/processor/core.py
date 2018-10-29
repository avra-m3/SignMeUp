import json
import os

import requests
from peewee import IntegrityError, DoesNotExist

from model.club import Club
from model.registration import Registration
from model.student import Student
from modules.ocr.process import get_card_data
from utilities.exception_router import APIException, Conflict


def handle_processing_errors(fn):
    """
    Wrap process with error handling to ensure the model is put in an erred
    state when an exception occurs
    :param fn: The function to wrap
    :return: the wrapped function
    :raises None: This function suppresses ALL exceptions
    """

    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except APIException as ex:
            print("Exception occurred while processing - {}".format(repr(ex)))
            raise
        except Exception as ex:
            print("Unexpected Exception occurred while processing - {}".format(repr(ex)))
            raise APIException()

    return wrapper


@handle_processing_errors
def process(image_location: str, user_id, club_name):
    try:
        student = Student.get_by_id(user_id)
        club, _ = Club.get_or_create(club_id=str(club_name))
    except DoesNotExist:
        data = request_ocr(image_location)
        card_data = get_card_data(user_id, data)

        print(card_data)

        student, _ = Student.get_or_create(**card_data)
        club, _ = Club.get_or_create(club_id=str(club_name))

    return Registration.create(student=student.user_id, club=club.club_id, proof=image_location)


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

    data = response.json()
    print(data)

    return data
