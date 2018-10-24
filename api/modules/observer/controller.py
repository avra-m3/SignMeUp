import json
import os
import re
import shutil
from base64 import b64encode

import requests

from modules.observer.processor_exceptions import UpstreamError, ProcessingException
from modules.path_constants import PATHS
from modules.recognition.ocr.process import get_card_data
from providers import provider


def process(path: str, file_id: str):
    """
    Calls and handles processing failures for files in PATHS.Queued directory
    :param path: The full path to the file
    :param file_id: The file id including extension.
    :return: None
    """
    try:
        begin_processing(path, file_id)
    except ProcessingException as ex:
        # A Processing Exception has occurred; these are expected to happen every now and again.

        # Move the file to the failed output directory.
        shutil.move(path, os.path.join(PATHS.FAIL, file_id))

        # Write an output file
        write_output(file_id,
                     status="failed",
                     message="{}, {}".format(ex.exc[0], ex.detail),
                     )

    except Exception as unexpected:
        # Something else happened; catch it and process the files as such
        ex_type = repr(unexpected).split("(")[0]
        write_output(file_id,
                     status="failed",
                     message="An unexpected {} occurred while processing the file.".format(ex_type),
                     )
        shutil.move(path, os.path.join(PATHS.FAIL, file_id))
    finally:
        print("Processing completed for {}".format(file_id))


def begin_processing(path: str, file_id: str):
    """
    This function handles the happy path (read successful) processing of files in the PATHS.Queued directory
    :param path: The full path to the file
    :param file_id: The file id including extension.
    :return: None
    """
    write_output(file_id,
                 status="processing",
                 message="File is processing",
                 )
    print("Requesting response for {}".format(file_id))
    # Get OCR response
    # response = request_ocr(path)

    print("Received response for {}".format(file_id))
    # print(response.content)
    data = fake_ocr()
    # data = response.json()

    # Check the response.
    if not data:  # or response.status_code != 200:
        raise UpstreamError("No Data Returned")

    # Get user_id by performing a regular expression match.
    user_id = re.match(".*21259(\d{7})\d{2}.*", file_id).groups()[0]

    # Perform operations on the data returned to pull the correct information
    data_obj = get_card_data(user_id, data)

    # Move file out of the queue
    shutil.move(path, os.path.join(PATHS.DONE, file_id))

    # Get the club/card id.
    write_output(file_id,
                 status="success",
                 message="file successfully processed",
                 first_name=data_obj["first_name"],
                 last_name=data_obj["last_name"],
                 )


def fake_ocr() -> dict:
    return json.loads(
        b'{"responses":[{"textAnnotations":[{"locale":"en","description":"Tyrel\\nCAMERON\\nMEMBER\\n3394330\\nExpiryDate:28/02/2020\\n21259339433010\\n","boundingPoly":{\n"vertices":[\n{\n"y":9\n},\n{\n"x":574,\n"y":9\n},\n{\n"x":574,\n"y":428\n},\n{\n"y":428\n}\n]\n}\n},\n{\n"description":"Tyrel",\n"boundingPoly":{\n"vertices":[\n{\n"x":34,\n"y":17\n},\n{\n"x":121,\n"y":9\n},\n{\n"x":124,\n"y":45\n},\n{\n"x":37,\n"y":53\n}\n]\n}\n},\n{\n"description":"CAMERON",\n"boundingPoly":{\n"vertices":[\n{\n"x":28,\n"y":78\n},\n{\n"x":232,\n"y":78\n},\n{\n"x":232,\n"y":108\n},\n{\n"x":28,\n"y":108\n}\n]\n}\n},\n{\n"description":"MEMBER",\n"boundingPoly":{\n"vertices":[\n{\n"x":468,\n"y":19\n},\n{\n"x":574,\n"y":28\n},\n{\n"x":571,\n"y":58\n},\n{\n"x":465,\n"y":49\n}\n]\n}\n},\n{\n"description":"3394330",\n"boundingPoly":{\n"vertices":[\n{\n"x":23,\n"y":184\n},\n{\n"x":182,\n"y":184\n},\n{\n"x":182,\n"y":214\n},\n{\n"x":23,\n"y":214\n}\n]\n}\n},\n{\n"description":"Expiry",\n"boundingPoly":{\n"vertices":[\n{\n"y":234\n},\n{\n"x":137,\n"y":234\n},\n{\n"x":137,\n"y":273\n},\n{\n"y":273\n}\n]\n}\n},\n{\n"description":"Date:",\n"boundingPoly":{\n"vertices":[\n{\n"x":152,\n"y":234\n},\n{\n"x":247,\n"y":234\n},\n{\n"x":247,\n"y":264\n},\n{\n"x":152,\n"y":264\n}\n]\n}\n},\n{\n"description":"28/02/2020",\n"boundingPoly":{\n"vertices":[\n{\n"x":260,\n"y":233\n},\n{\n"x":459,\n"y":233\n},\n{\n"x":459,\n"y":264\n},\n{\n"x":260,\n"y":264\n}\n]\n}\n},\n{\n"description":"21259339433010",\n"boundingPoly":{\n"vertices":[\n{\n"x":220,\n"y":402\n},\n{\n"x":471,\n"y":397\n},\n{\n"x":471,\n"y":423\n},\n{\n"x":220,\n"y":428\n}\n]\n}\n}\n],\n"fullTextAnnotation":{\n"pages":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"width":640,\n"height":480,\n"blocks":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"no"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":28,\n"y":9\n},\n{\n"x":232,\n"y":9\n},\n{\n"x":232,\n"y":108\n},\n{\n"x":28,\n"y":108\n}\n]\n},\n"paragraphs":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"no"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":28,\n"y":9\n},\n{\n"x":232,\n"y":9\n},\n{\n"x":232,\n"y":108\n},\n{\n"x":28,\n"y":108\n}\n]\n},\n"words":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"no"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":34,\n"y":17\n},\n{\n"x":121,\n"y":9\n},\n{\n"x":124,\n"y":45\n},\n{\n"x":37,\n"y":53\n}\n]\n},\n"symbols":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":34,\n"y":17\n},\n{\n"x":56,\n"y":15\n},\n{\n"x":58,\n"y":43\n},\n{\n"x":36,\n"y":45\n}\n]\n},\n"text":"T"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":57,\n"y":24\n},\n{\n"x":76,\n"y":22\n},\n{\n"x":78,\n"y":49\n},\n{\n"x":59,\n"y":51\n}\n]\n},\n"text":"y"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":77,\n"y":22\n},\n{\n"x":91,\n"y":21\n},\n{\n"x":93,\n"y":42\n},\n{\n"x":79,\n"y":43\n}\n]\n},\n"text":"r"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":90,\n"y":18\n},\n{\n"x":105,\n"y":17\n},\n{\n"x":107,\n"y":43\n},\n{\n"x":92,\n"y":44\n}\n]\n},\n"text":"e"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n],\n"detectedBreak":{\n"type":"EOL_SURE_SPACE"\n}\n},\n"boundingBox":{\n"vertices":[\n{\n"x":106,\n"y":17\n},\n{\n"x":121,\n"y":16\n},\n{\n"x":123,\n"y":42\n},\n{\n"x":108,\n"y":43\n}\n]\n},\n"text":"l"\n}\n]\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":28,\n"y":78\n},\n{\n"x":232,\n"y":78\n},\n{\n"x":232,\n"y":108\n},\n{\n"x":28,\n"y":108\n}\n]\n},\n"symbols":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":28,\n"y":78\n},\n{\n"x":52,\n"y":78\n},\n{\n"x":52,\n"y":107\n},\n{\n"x":28,\n"y":107\n}\n]\n},\n"text":"C"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":53,\n"y":78\n},\n{\n"x":80,\n"y":78\n},\n{\n"x":80,\n"y":107\n},\n{\n"x":53,\n"y":107\n}\n]\n},\n"text":"A"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":83,\n"y":78\n},\n{\n"x":114,\n"y":78\n},\n{\n"x":114,\n"y":107\n},\n{\n"x":83,\n"y":107\n}\n]\n},\n"text":"M"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":117,\n"y":78\n},\n{\n"x":142,\n"y":78\n},\n{\n"x":142,\n"y":107\n},\n{\n"x":117,\n"y":107\n}\n]\n},\n"text":"E"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":145,\n"y":78\n},\n{\n"x":171,\n"y":78\n},\n{\n"x":171,\n"y":107\n},\n{\n"x":145,\n"y":107\n}\n]\n},\n"text":"R"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":174,\n"y":78\n},\n{\n"x":204,\n"y":78\n},\n{\n"x":204,\n"y":107\n},\n{\n"x":174,\n"y":107\n}\n]\n},\n"text":"O"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n],\n"detectedBreak":{\n"type":"EOL_SURE_SPACE"\n}\n},\n"boundingBox":{\n"vertices":[\n{\n"x":207,\n"y":79\n},\n{\n"x":232,\n"y":79\n},\n{\n"x":232,\n"y":108\n},\n{\n"x":207,\n"y":108\n}\n]\n},\n"text":"N"\n}\n]\n}\n]\n}\n],\n"blockType":"TEXT"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":465,\n"y":19\n},\n{\n"x":574,\n"y":19\n},\n{\n"x":574,\n"y":58\n},\n{\n"x":465,\n"y":58\n}\n]\n},\n"paragraphs":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":465,\n"y":19\n},\n{\n"x":574,\n"y":19\n},\n{\n"x":574,\n"y":58\n},\n{\n"x":465,\n"y":58\n}\n]\n},\n"words":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":468,\n"y":19\n},\n{\n"x":574,\n"y":28\n},\n{\n"x":571,\n"y":58\n},\n{\n"x":465,\n"y":49\n}\n]\n},\n"symbols":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":468,\n"y":19\n},\n{\n"x":490,\n"y":21\n},\n{\n"x":487,\n"y":51\n},\n{\n"x":465,\n"y":49\n}\n]\n},\n"text":"M"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":491,\n"y":21\n},\n{\n"x":506,\n"y":22\n},\n{\n"x":503,\n"y":52\n},\n{\n"x":488,\n"y":51\n}\n]\n},\n"text":"E"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":507,\n"y":22\n},\n{\n"x":527,\n"y":24\n},\n{\n"x":524,\n"y":54\n},\n{\n"x":504,\n"y":52\n}\n]\n},\n"text":"M"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":528,\n"y":24\n},\n{\n"x":548,\n"y":26\n},\n{\n"x":545,\n"y":56\n},\n{\n"x":525,\n"y":54\n}\n]\n},\n"text":"B"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":549,\n"y":26\n},\n{\n"x":558,\n"y":27\n},\n{\n"x":555,\n"y":57\n},\n{\n"x":546,\n"y":56\n}\n]\n},\n"text":"E"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n],\n"detectedBreak":{\n"type":"EOL_SURE_SPACE"\n}\n},\n"boundingBox":{\n"vertices":[\n{\n"x":559,\n"y":27\n},\n{\n"x":574,\n"y":28\n},\n{\n"x":571,\n"y":58\n},\n{\n"x":556,\n"y":57\n}\n]\n},\n"text":"R"\n}\n]\n}\n]\n}\n],\n"blockType":"TEXT"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":23,\n"y":184\n},\n{\n"x":182,\n"y":184\n},\n{\n"x":182,\n"y":214\n},\n{\n"x":23,\n"y":214\n}\n]\n},\n"paragraphs":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":23,\n"y":184\n},\n{\n"x":182,\n"y":184\n},\n{\n"x":182,\n"y":214\n},\n{\n"x":23,\n"y":214\n}\n]\n},\n"words":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":23,\n"y":184\n},\n{\n"x":182,\n"y":184\n},\n{\n"x":182,\n"y":214\n},\n{\n"x":23,\n"y":214\n}\n]\n},\n"symbols":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":23,\n"y":185\n},\n{\n"x":42,\n"y":185\n},\n{\n"x":42,\n"y":214\n},\n{\n"x":23,\n"y":214\n}\n]\n},\n"text":"3"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":45,\n"y":184\n},\n{\n"x":65,\n"y":184\n},\n{\n"x":65,\n"y":214\n},\n{\n"x":45,\n"y":214\n}\n]\n},\n"text":"3"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":67,\n"y":184\n},\n{\n"x":88,\n"y":184\n},\n{\n"x":88,\n"y":214\n},\n{\n"x":67,\n"y":214\n}\n]\n},\n"text":"9"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":90,\n"y":185\n},\n{\n"x":111,\n"y":185\n},\n{\n"x":111,\n"y":214\n},\n{\n"x":90,\n"y":214\n}\n]\n},\n"text":"4"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":114,\n"y":184\n},\n{\n"x":135,\n"y":184\n},\n{\n"x":135,\n"y":214\n},\n{\n"x":114,\n"y":214\n}\n]\n},\n"text":"3"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":138,\n"y":184\n},\n{\n"x":157,\n"y":184\n},\n{\n"x":157,\n"y":214\n},\n{\n"x":138,\n"y":214\n}\n]\n},\n"text":"3"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n],\n"detectedBreak":{\n"type":"EOL_SURE_SPACE"\n}\n},\n"boundingBox":{\n"vertices":[\n{\n"x":160,\n"y":184\n},\n{\n"x":182,\n"y":184\n},\n{\n"x":182,\n"y":214\n},\n{\n"x":160,\n"y":214\n}\n]\n},\n"text":"0"\n}\n]\n}\n]\n}\n],\n"blockType":"TEXT"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"af"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"y":233\n},\n{\n"x":459,\n"y":233\n},\n{\n"x":459,\n"y":273\n},\n{\n"y":273\n}\n]\n},\n"paragraphs":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"af"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"y":233\n},\n{\n"x":459,\n"y":233\n},\n{\n"x":459,\n"y":273\n},\n{\n"y":273\n}\n]\n},\n"words":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"y":234\n},\n{\n"x":137,\n"y":234\n},\n{\n"x":137,\n"y":273\n},\n{\n"y":273\n}\n]\n},\n"symbols":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"y":235\n},\n{\n"x":45,\n"y":235\n},\n{\n"x":45,\n"y":265\n},\n{\n"y":265\n}\n]\n},\n"text":"E"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":46,\n"y":242\n},\n{\n"x":68,\n"y":242\n},\n{\n"x":68,\n"y":273\n},\n{\n"x":46,\n"y":273\n}\n]\n},\n"text":"x"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":69,\n"y":242\n},\n{\n"x":92,\n"y":242\n},\n{\n"x":92,\n"y":273\n},\n{\n"x":69,\n"y":273\n}\n]\n},\n"text":"p"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":94,\n"y":234\n},\n{\n"x":100,\n"y":234\n},\n{\n"x":100,\n"y":265\n},\n{\n"x":94,\n"y":265\n}\n]\n},\n"text":"i"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":104,\n"y":242\n},\n{\n"x":120,\n"y":242\n},\n{\n"x":120,\n"y":273\n},\n{\n"x":104,\n"y":273\n}\n]\n},\n"text":"r"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n],\n"detectedBreak":{\n"type":"SPACE"\n}\n},\n"boundingBox":{\n"vertices":[\n{\n"x":121,\n"y":242\n},\n{\n"x":137,\n"y":242\n},\n{\n"x":137,\n"y":273\n},\n{\n"x":121,\n"y":273\n}\n]\n},\n"text":"y"\n}\n]\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"af"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":152,\n"y":234\n},\n{\n"x":247,\n"y":234\n},\n{\n"x":247,\n"y":264\n},\n{\n"x":152,\n"y":264\n}\n]\n},\n"symbols":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":152,\n"y":234\n},\n{\n"x":179,\n"y":234\n},\n{\n"x":179,\n"y":264\n},\n{\n"x":152,\n"y":264\n}\n]\n},\n"text":"D"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":182,\n"y":236\n},\n{\n"x":197,\n"y":236\n},\n{\n"x":197,\n"y":264\n},\n{\n"x":182,\n"y":264\n}\n]\n},\n"text":"a"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":198,\n"y":236\n},\n{\n"x":214,\n"y":236\n},\n{\n"x":214,\n"y":264\n},\n{\n"x":198,\n"y":264\n}\n]\n},\n"text":"t"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":216,\n"y":241\n},\n{\n"x":237,\n"y":241\n},\n{\n"x":237,\n"y":264\n},\n{\n"x":216,\n"y":264\n}\n]\n},\n"text":"e"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n],\n"detectedBreak":{\n"type":"SPACE"\n}\n},\n"boundingBox":{\n"vertices":[\n{\n"x":241,\n"y":242\n},\n{\n"x":247,\n"y":242\n},\n{\n"x":247,\n"y":264\n},\n{\n"x":241,\n"y":264\n}\n]\n},\n"text":":"\n}\n]\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":260,\n"y":233\n},\n{\n"x":459,\n"y":233\n},\n{\n"x":459,\n"y":264\n},\n{\n"x":260,\n"y":264\n}\n]\n},\n"symbols":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":260,\n"y":233\n},\n{\n"x":281,\n"y":233\n},\n{\n"x":281,\n"y":264\n},\n{\n"x":260,\n"y":264\n}\n]\n},\n"text":"2"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":283,\n"y":233\n},\n{\n"x":304,\n"y":233\n},\n{\n"x":304,\n"y":264\n},\n{\n"x":283,\n"y":264\n}\n]\n},\n"text":"8"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":304,\n"y":233\n},\n{\n"x":316,\n"y":233\n},\n{\n"x":316,\n"y":263\n},\n{\n"x":304,\n"y":263\n}\n]\n},\n"text":"/"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":318,\n"y":233\n},\n{\n"x":337,\n"y":233\n},\n{\n"x":337,\n"y":263\n},\n{\n"x":318,\n"y":263\n}\n]\n},\n"text":"0"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":339,\n"y":233\n},\n{\n"x":355,\n"y":233\n},\n{\n"x":355,\n"y":264\n},\n{\n"x":339,\n"y":264\n}\n]\n},\n"text":"2"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":356,\n"y":233\n},\n{\n"x":372,\n"y":233\n},\n{\n"x":372,\n"y":264\n},\n{\n"x":356,\n"y":264\n}\n]\n},\n"text":"/"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":372,\n"y":233\n},\n{\n"x":393,\n"y":233\n},\n{\n"x":393,\n"y":263\n},\n{\n"x":372,\n"y":263\n}\n]\n},\n"text":"2"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":395,\n"y":233\n},\n{\n"x":416,\n"y":233\n},\n{\n"x":416,\n"y":263\n},\n{\n"x":395,\n"y":263\n}\n]\n},\n"text":"0"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":417,\n"y":233\n},\n{\n"x":437,\n"y":233\n},\n{\n"x":437,\n"y":263\n},\n{\n"x":417,\n"y":263\n}\n]\n},\n"text":"2"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n],\n"detectedBreak":{\n"type":"EOL_SURE_SPACE"\n}\n},\n"boundingBox":{\n"vertices":[\n{\n"x":438,\n"y":233\n},\n{\n"x":459,\n"y":233\n},\n{\n"x":459,\n"y":263\n},\n{\n"x":438,\n"y":263\n}\n]\n},\n"text":"0"\n}\n]\n}\n]\n}\n],\n"blockType":"TEXT"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":220,\n"y":397\n},\n{\n"x":471,\n"y":397\n},\n{\n"x":471,\n"y":428\n},\n{\n"x":220,\n"y":428\n}\n]\n},\n"paragraphs":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":220,\n"y":397\n},\n{\n"x":471,\n"y":397\n},\n{\n"x":471,\n"y":428\n},\n{\n"x":220,\n"y":428\n}\n]\n},\n"words":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":220,\n"y":402\n},\n{\n"x":471,\n"y":397\n},\n{\n"x":471,\n"y":423\n},\n{\n"x":220,\n"y":428\n}\n]\n},\n"symbols":[\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":220,\n"y":402\n},\n{\n"x":237,\n"y":402\n},\n{\n"x":237,\n"y":428\n},\n{\n"x":220,\n"y":428\n}\n]\n},\n"text":"2"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":240,\n"y":403\n},\n{\n"x":250,\n"y":403\n},\n{\n"x":250,\n"y":428\n},\n{\n"x":240,\n"y":428\n}\n]\n},\n"text":"1"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":257,\n"y":401\n},\n{\n"x":274,\n"y":401\n},\n{\n"x":274,\n"y":427\n},\n{\n"x":257,\n"y":427\n}\n]\n},\n"text":"2"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":275,\n"y":401\n},\n{\n"x":291,\n"y":401\n},\n{\n"x":291,\n"y":426\n},\n{\n"x":275,\n"y":426\n}\n]\n},\n"text":"5"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":292,\n"y":401\n},\n{\n"x":310,\n"y":401\n},\n{\n"x":310,\n"y":426\n},\n{\n"x":292,\n"y":426\n}\n]\n},\n"text":"9"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":311,\n"y":401\n},\n{\n"x":328,\n"y":401\n},\n{\n"x":328,\n"y":425\n},\n{\n"x":311,\n"y":425\n}\n]\n},\n"text":"3"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":329,\n"y":400\n},\n{\n"x":346,\n"y":400\n},\n{\n"x":346,\n"y":425\n},\n{\n"x":329,\n"y":425\n}\n]\n},\n"text":"3"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":347,\n"y":401\n},\n{\n"x":363,\n"y":401\n},\n{\n"x":363,\n"y":425\n},\n{\n"x":347,\n"y":425\n}\n]\n},\n"text":"9"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":364,\n"y":400\n},\n{\n"x":381,\n"y":400\n},\n{\n"x":381,\n"y":424\n},\n{\n"x":364,\n"y":424\n}\n]\n},\n"text":"4"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":382,\n"y":400\n},\n{\n"x":399,\n"y":400\n},\n{\n"x":399,\n"y":424\n},\n{\n"x":382,\n"y":424\n}\n]\n},\n"text":"3"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":400,\n"y":400\n},\n{\n"x":417,\n"y":400\n},\n{\n"x":417,\n"y":424\n},\n{\n"x":400,\n"y":424\n}\n]\n},\n"text":"3"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":418,\n"y":399\n},\n{\n"x":435,\n"y":399\n},\n{\n"x":435,\n"y":423\n},\n{\n"x":418,\n"y":423\n}\n]\n},\n"text":"0"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n]\n},\n"boundingBox":{\n"vertices":[\n{\n"x":438,\n"y":399\n},\n{\n"x":454,\n"y":399\n},\n{\n"x":454,\n"y":423\n},\n{\n"x":438,\n"y":423\n}\n]\n},\n"text":"1"\n},\n{\n"property":{\n"detectedLanguages":[\n{\n"languageCode":"en"\n}\n],\n"detectedBreak":{\n"type":"EOL_SURE_SPACE"\n}\n},\n"boundingBox":{\n"vertices":[\n{\n"x":455,\n"y":399\n},\n{\n"x":471,\n"y":399\n},\n{\n"x":471,\n"y":423\n},\n{\n"x":455,\n"y":423\n}\n]\n},\n"text":"0"\n}\n]\n}\n]\n}\n],\n"blockType":"TEXT"\n}\n]\n}\n],\n"text":"Tyrel\\nCAMERON\\nMEMBER\\n3394330\\nExpiryDate:28/02/2020\\n21259339433010\\n"\n}\n}\n]\n}\n')


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


def write_output(file_id, **kwargs):
    """
    Write an output file for a given id
    :param status: One of (success, failed, created, processing)
    :param message: A short string message that describes what happened
    :param result: Addition information about this result
    :param file_id: The file id
    :return: None
    """
    club_id, card_id = re.match("(\w+)_(21259\d{7}\d{2})", file_id).groups()
    club = provider.club(club_id)
    registration = provider.registration(club, card_id)
    for key in kwargs:
        if hasattr(registration, key):
            setattr(registration, key, kwargs[key])
    registration.update()
