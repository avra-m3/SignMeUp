import json
import os
from base64 import b64encode

import requests


def begin_processing(path: str):
    response = request_ocr(path)


def request_ocr(path: str):
    ENDPOINT = 'https://vision.googleapis.com/v1/images:annotate'
    AUTH = os.getenv('OCR_AUTH_KEY')
    HEADERS = {'Content-Type': 'application/json'}
    with open(path, "rb") as image:
        contents = image.read()
        return requests.post(ENDPOINT,
                             data=json.dumps(
                                 {
                                     'requests': [{
                                         'image': {'content': b64encode(contents).decode()},
                                         "features": [
                                             {
                                                 "type": "TEXT_DETECTION"
                                             }
                                         ],
                                         "imageContext": {
                                             "languageHints": [
                                                 "en"
                                             ]
                                         }
                                     }]
                                 }
                             ),
                             params={'key': AUTH},
                             headers=HEADERS
                             )
