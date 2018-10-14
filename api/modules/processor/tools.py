import json
import os
import re
import shutil
from base64 import b64encode

import requests

from modules.image_processing.ocr.process import get_card_data
from modules.objects import PATHS
from modules.processor.processor_exceptions import UpstreamError, ProcessingException


def process(path: str, file_id: str):
    try:
        begin_processing(path, file_id)
    except ProcessingException as ex:
        print("EXCEPTION: {}".format(ex.exc))
        with open(os.path.join(PATHS.FAIL, file_id) + ".json", "w") as error_file:
            error_file.write(ex.json)
        shutil.copy(path, os.path.join(PATHS.FAIL, file_id))
        os.remove(path)


def begin_processing(path: str, file_id: str):
    print("Requesting response for {}".format(file_id))
    response = request_ocr(path)
    print("Received response for {}".format(file_id))
    print(response.content)
    data = response.json()

    user_id = re.match("21259(\d{7})\d{2}", file_id).groups()[0]
    if not data or response.status_code != 200:
        raise UpstreamError("No Data Returned")
    data_obj = get_card_data(user_id, data)
    print(data_obj)
    shutil.move(path, os.path.join(PATHS.DONE, file_id))
    with open(os.path.join(PATHS.DONE, file_id + ".json"), "w") as output:
        output.write(json.dumps(data_obj))


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
