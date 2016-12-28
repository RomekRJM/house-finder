# -*- coding: utf-8 -*-
__author__ = "roman.subik"

import re


def normalize_number(obj, type='int'):

    if isinstance(obj, (int, float)):
        return obj

    search = re.search("[0-9\.,\s]+", obj)

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
