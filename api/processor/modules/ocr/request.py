import json
import os
import warnings
from typing import List

import requests
from google.cloud import vision

from utilities.exception_router import APIException


def legacy_request_ocr(url: str) -> List[dict]:
    """
    Requests OCR data from google cloud.
    This function requires an environment variable with the key 'OCR_AUTH_KEY';
    The values should be an api key with access to google's text detection api
    :return: An object like a List of dictionary.
    :deprecated: in favour of request_ocr
    """

    warnings.warn(
        "Call to deprecated method 'legacy_request_ocr' this method is no longer supported, use 'request_ocr' instead")
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
    return data["responses"][0]["textAnnotations"][1:]


def request_ocr(url: str) -> list:
    client = vision.ImageAnnotatorClient()
    try:
        response = client.annotate_image({
            "image": {
                "source": {
                    "image_uri": url,
                }
            },
            "features": [
                {"type": vision.enums.Feature.Type.TEXT_DETECTION}
            ],
        })
        if not response.text_annotations:
            raise RuntimeError(str(response))
    except Exception:
        raise APIException("Upstream gateway returned an unacceptable response", status=502)
    return response_as_dict(response.text_annotations)


def response_as_dict(annotations) -> List[dict]:
    """
    Adapt the google cloud response to a dictionary.
    :param annotations:
    :return:
    """
    result = []
    for entity in annotations:
        temp = {
            "description": entity.description,
            "bounding_poly": {'vertices': [{'x': coord.x, 'y': coord.y} for coord in entity.bounding_poly.vertices]},
        }
        result.append(temp)
    return result
