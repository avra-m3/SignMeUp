import re
from typing import List, Tuple

from modules.ocr.fields import TextField
from utilities.exception_router import Conflict, APIException


def get_card_data(user_id: str, data: dict) -> dict:
    text_data = data["responses"][0]["textAnnotations"][1:]
    print("Analysing Data for s{}".format(user_id))
    user_id_field = get_user_id(user_id, text_data)
    fname_fields, lname_fields = get_name_fields(text_data)
    fname_fields = order_names(fname_fields, user_id_field)
    lname_fields = order_names(lname_fields, user_id_field)

    user_id = str(user_id_field)
    first_name = " ".join([str(f) for f in fname_fields])
    last_name = " ".join([str(l).lower().capitalize() for l in lname_fields])

    return {"user_id": user_id, "first_name": first_name, "last_name": last_name}


def get_user_id(user_id: str, data: dict) -> TextField:
    result = None
    matcher = re.compile("^{}$".format(user_id))
    for field in data:
        temp = TextField(field, "Student ID", matcher=matcher)
        if temp.is_valid_field():
            if result is not None:
                raise Conflict("The {} field received duplicate values".format("Student ID"))
            result = temp
    if result is None:
        raise APIException("Unable to identify a {} field".format("Student ID"))
    return result


def get_name_fields(data: dict) -> Tuple[List[TextField], List[TextField]]:
    first = []
    last = []
    fname_matcher = re.compile('^((?!Expiry)[A-Z][a-z\-]+)$')
    lname_matcher = re.compile('^([A-Z\-]+)$')
    for field in data:
        as_first_name = TextField(field, "First Name", matcher=fname_matcher)
        as_last_name = TextField(field, "Last Name", matcher=lname_matcher)
        if as_first_name.is_valid_field():
            first.append(as_first_name)
        elif as_last_name.is_valid_field():
            last.append(as_last_name)
    if first and last:
        return first, last
    if not first and not last:
        raise APIException("Unable to identify a name field")
    if not first:
        raise APIException("Unable to identify a first name field")
    if not last:
        raise APIException("Unable to identify a last name field")


def order_names(fields: List[TextField], above_field: TextField):
    unsorted = fields.copy()
    ordered = []
    head = above_field
    flag = True
    while flag:
        flag = False
        field = (list(filter(head.adjacent_to, unsorted)) or [None])[0]
        if field is not None and head.adjacent_to(field):
            head = field
            flag = True
        if not flag:
            for field in sorted(filter(above_field.is_above, unsorted), key=above_field.v_distance_to):
                head = field
                flag = True
                break
        if flag:
            ordered.append(head)
            unsorted.remove(head)
    return ordered
