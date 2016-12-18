__author__ = "roman.subik"

import re


def normalize_number(str_repr):
    search = re.search("[0-9\.,\s]+", str_repr)

    try:
        number = search.group(0)
        number = number.replace(' ', '')
        number = number.replace(',', '.')
    except AttributeError as ae:
        return None

    if "." in number or "," in number:
        return float(number)

    return int(number)


def normalize_string(str_rep):
    return str_rep.decode('unicode_escape').strip()