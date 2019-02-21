import re

import cv2
import pytesseract
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
    thresh = (255-thresh)
    cv2.imshow("thresh", thresh)
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
    print(pytesseract.image_to_data(thresh))


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


if __name__ == "__main__":
    optimize(cv2.imread("C:\\Users\\avram\\PycharmProjects\\csit_student_signup\\cache\\20180719114310.temp.png"))
    k = cv2.waitKey(0)
