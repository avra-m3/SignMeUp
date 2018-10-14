import re
from typing import List, Tuple

from modules.image_processing.ocr.fields import TextField
from modules.processor.processor_exceptions import ConflictError, FieldError


def get_card_data(user_id: str, data: dict) -> dict:
    text_data = data["responses"][0]["textAnnotations"][1:]
    user_id_field = get_user_id(user_id, text_data)
    fname_fields, lname_fields = get_name_fields(text_data)
    fname_fields = order_names(fname_fields, user_id_field)
    lname_fields = order_names(lname_fields, fname_fields[-1])

    user_id = str(user_id_field)
    first_name = " ".join([str(f) for f in fname_fields])
    last_name = " ".join([str(l).lower().capitalize() for l in lname_fields])

    return {"user_id": user_id, "first": first_name, "last": last_name}


def get_user_id(user_id: str, data: dict) -> TextField:
    result = None
    matcher = re.compile("^{}$".format(user_id))
    for field in data:
        temp = TextField(field, "Student ID", matcher=matcher)
        if temp.is_valid_field():
            if result is not None:
                raise ConflictError("The {} field received duplicate values".format("Student ID"))
            result = temp
    if result is None:
        raise FieldError("Unable to identify a {} field".format("Student ID"))
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
        raise FieldError("Unable to identify a name field")
    if not first:
        raise FieldError("Unable to identify a first name field")
    if not last:
        raise FieldError("Unable to identify a last name field")


def order_names(fields: List[TextField], head: TextField):
    unsorted = []
    for field in fields:
        if head.is_above(field):
            unsorted.append(field)

    ordered = []
    while len(unsorted) > 0:
        flag = False
        for field in sorted(unsorted, key=head.v_distance_to):
            if field.adjacent_to(head):
                head = field
                flag = True
                break
        if not flag:
            head = sorted(unsorted, key=head.v_distance_to)[0]
        ordered.append(head)
        unsorted.remove(head)

    return ordered
