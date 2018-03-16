# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from spiders.utils import normalize_number

field_mappings = {
    u"Informacje dodatkowe": ("additional_info"),
    u"Media": ("utilities"),
    u"Wyposażenie": ("furnishings"),
    u"Czynsz": ("rent", normalize_number),
    u"Dostępne od": ("available_from"),
    u"Forma własności": ("ownership"),
    u"Materiał budynku": ("construction_material"),
    u"Ogrzewanie": ("heating"),
    u"Okna": ("windows"),
    u"Rodzaj zabudowy": ("building_type"),
    u"Rok budowy": ("year_built", normalize_number),
    u"Rynek": ("market"),
    u"Stan wykończenia": ("building_state"),
    u"Zabezpieczenia": ("security")
}


class PropertyItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    date_added = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
    num_rooms = scrapy.Field()
    floor = scrapy.Field()
    price_per_sqm = scrapy.Field()
    location = scrapy.Field()
    additional_info = scrapy.Field()
    utilities = scrapy.Field()
    furnishings = scrapy.Field()
    rent = scrapy.Field()
    available_from = scrapy.Field()
    ownership = scrapy.Field()
    construction_material = scrapy.Field()
    heating = scrapy.Field()
    windows = scrapy.Field()
    building_type = scrapy.Field()
    year_built = scrapy.Field()
    market = scrapy.Field()
    building_state = scrapy.Field()
    security = scrapy.Field()
    images = scrapy.Field()
    notified_on = scrapy.Field()

    def set_field(self, polish_field_name, field_value):
        mapping = field_mappings[polish_field_name]

        if isinstance(mapping, tuple):
            english_field_name = mapping[0]
            cast_function = mapping[1]
            field_value = cast_function(field_value)
        else:
            english_field_name = mapping

        self[english_field_name] = field_value
