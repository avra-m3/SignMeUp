import re

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

from utilities.exception_router import PreconditionFailed, NotAcceptable

valid_bacode_format = re.compile("^\d{14}$")


def optimize(image):
    """
    Experimental method to optimize barcode detection
    :param image: The cv2 image
    :return:
    """
    cv2.imshow("original", image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imshow("thresh", thresh)
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    print(angle)


def decode(im):
    """
    Process the image and decode the first located barcode
    :param im:
    :return:
    """
    barcodes = pyzbar.decode(im)
    valid_barcodes = [b for b in barcodes if b.type == "CODE39" and valid_bacode_format.match(b.data.decode())]
    if len(valid_barcodes) != 1:
        raise PreconditionFailed("Unable to identify a valid barcode in the given Image.")
    return valid_barcodes[0].data.decode()


def process(path: str) -> str:
    """
    Process an image from the path to the file
    :param path:
    :return:
    """
    # Read image
    im = cv2.imread(path)
    if im is None:
        raise NotAcceptable("Uploaded file was in an invalid format.")
    return decode(im)

