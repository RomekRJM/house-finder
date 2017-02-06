# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


field_mappings = {
    u"informacje dodatkowe": "additional_info",
    u"media": "utilities",
    u"wyposażenie": "furnishings",
    u"czynsz": "rent",
    u"dostępne od": "available_from",
    u"forma własności": "ownership",
    u"materiał budynku": "construction_material",
    u"ogrzewanie": "heating",
    u"okna": "windows",
    u"rodzaj zabudowy": "building_type",
    u"rok budowy": "year_built",
    u"rynek": "market",
    u"stan wykończenia": "building_state",
    u"zabezpieczenia": "security"
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
        self[field_mappings[polish_field_name]] = field_value