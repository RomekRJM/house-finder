# -*- coding: utf-8 -*-
__author__ = "roman.subik"

import re


def normalize_number(str_repr, type='int'):
    search = re.search("[0-9\.,\s]+", str_repr)

    try:
        number = search.group(0)
        number = number.replace(' ', '')
        number = number.replace(',', '.')
    except AttributeError as ae:
        return None

    if "." in number or "," in number or type == 'float':
        return float(number)

    return int(number)


def normalize_string(str_rep):
    if str_rep:
        return str_rep.replace(":", "").strip()

    return str_rep
