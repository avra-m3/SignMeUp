import json
import os
import re
from typing import List, Union

import requests
from google.cloud import vision
from google.cloud.vision_v1.proto.image_annotator_pb2 import EntityAnnotation
from google.cloud.vision_v1.types

from utilities.exception_router import APIException


def legacy_request_ocr(url: str) -> List[dict]:
    """
    Requests OCR data from google cloud.
    This function requires an environment variable with the key 'OCR_AUTH_KEY';
    The values should be an api key with access to google's text detection api
    :return: An object like a List of dictionary.
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
    return LegacyOCRRequestAdapter(data["responses"][0]["textAnnotations"][1:])


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
            raise RuntimeError()
    except Exception:
        raise APIException("Upstream gateway returned an unacceptable response", status=502)
    return response.text_annotations


class GCloudResponseAdapter:
    class GCloudContainer(list):
        def __init__(self, container):
            new = []
            for item in container:
                if isinstance(item, EntityAnnotation):
                    new.append()

    class GCloudAnnotation(dict):
        def __init__(self):
            pass

    def create(self, response: list):
        return self.GCloudContainer(response)


class LegacyOCRRequestAdapter:
    """
    This class will allow us to continue using the legacy request response object
    despite the difference in key names.
    ie boundingPoly -> bounding_poly
    """
    _obj: Union[list, dict]

    _rx = r"(.*?)_([a-zA-Z])"

    def __init__(self, response: Union[list, dict]):
        temp = None
        print(type(response))
        if isinstance(response, list):
            temp = []
            for item in response:
                if isinstance(item, dict) or isinstance(item, list):
                    temp.append(LegacyOCRRequestAdapter(item))
                else:
                    temp.append(item)
        elif isinstance(response, dict):
            temp = {}
            for key in response:
                item = response[key]
                if isinstance(item, dict) or isinstance(item, list):
                    temp[key] = LegacyOCRRequestAdapter(item)
                else:
                    temp[key] = item
        print(temp)
        self._obj = temp

    def _camel_case(self, match):
        """
        Given a match, return the camelCase version of the string
        :param match:
        :return:
        """
        return match.group(1) + match.group(2).upper()

    def __getitem__(self, item):
        """
        Override getitem to lookup the snake case string as camel case when it doesn't exist
        :param item: The key or index to lookup
        :return: Any
        """
        if isinstance(self._obj, list):
            return self._obj[item]
        elif isinstance(self._obj, dict):
            if item in self._obj:
                return self._obj[item]
            else:
                item = re.sub(self._rx, self._camel_case, item, 0)
                return self._obj[item]

    def __iter__(self):
        return iter(self._obj)

    def __len__(self):
        return len(self._obj)

    def keys(self):
        if isinstance(self._obj, dict):
            return self._obj.keys()

    def items(self):
        return self._obj.items()
