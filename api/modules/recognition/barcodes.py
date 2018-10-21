import re

import cv2
import pyzbar.pyzbar as pyzbar

from utilities.exception_router import PreconditionFailed

valid_bacode_format = re.compile("^\d{14}$")


def decode(im):
    barcodes = pyzbar.decode(im)
    valid_barcodes = [b for b in barcodes if b.type == "CODE39" and valid_bacode_format.match(b.data.decode())]
    if len(valid_barcodes) != 1:
        raise PreconditionFailed("Unable to identify a valid barcode in the given Image.")
    return valid_barcodes[0].data.decode()


def process(path: str) -> str:
    # Read image
    im = cv2.imread(path)
    if im is None:
        raise PreconditionFailed("Uploaded file was in an invalid format.")
    return decode(im)
