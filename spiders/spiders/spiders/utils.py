# -*- coding: utf-8 -*-
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
    try:
        return str_rep.replace(":", "").replace(u'\xc3', u'ó').replace(u'\u0142', u'ł')\
            .replace(u'\u015b', u'ś').strip()
    except TypeError as e:
        return str_rep
