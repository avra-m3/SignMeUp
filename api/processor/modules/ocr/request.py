import json
import os
import re
from typing import List

import requests
from google.cloud import vision
from google.cloud.vision_v1.proto.image_annotator_pb2 import AnnotateImageResponse

from utilities.exception_router import APIException


def request_ocr(url: str) -> List[dict]:
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
    output = data["responses"][0]["textAnnotations"][1:]


def to_snake_case(output: List[dict]) -> List[dict]:
    as_str = json.dumps(output)
    s1 = re.sub("(.)([A-Z][a-z]+)", r'\1_\2', as_str)
    s2 = re.sub("([a-z0-9])(A-Z)", r'\1_\2', s1).lower()
    return json.loads(s2)


def __future__request_ocr(url: str) -> list:
    client = vision.ImageAnnotatorClient()
    try:
        response: AnnotateImageResponse = client.annotate_image({
            "image": {
                "source": {
                    "image_uri": url,
                }
            },
            "features": [
                {"type": vision.enums.Feature.Type.TEXT_DETECTION}
            ],
            # "imageContext": {
            #     "languageHints": [
            #         "en"
            #     ]
            # }
        })
        if not response.text_annotations:
            raise RuntimeError()
    except Exception:
        raise APIException("Upstream gateway returned an unacceptable response", status=502)
    return response.text_annotations
