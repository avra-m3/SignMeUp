import tempfile

from flask import request

from utilities.exception_router import NotAcceptable


def safely_accept_file():
    # Confirm the form data includes a key for 'student_card'
    if 'student_card' not in request.files:
        raise NotAcceptable("No student_card file parameter was parsed as part of the request.")
    upload = request.files['student_card']

    # Check the file is not empty (This is caused by the browser)
    if upload.filename == '':
        raise NotAcceptable("The file passed had no file name")

    # Make a temporary file and write the upload to it.
    temp = tempfile.NamedTemporaryFile()
    temp.close()

    upload.save(temp.name)

    return temp.name
