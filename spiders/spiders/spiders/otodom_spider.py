__author__ = "roman.subik"

import re

import scrapy
from spiders.items import PropertyItem

from .utils import normalize_number, normalize_string

GEO_LOCATION_PATTERN = re.compile('"latitude":([0-9]+.[0-9]+),"longitude":([0-9]+.[0-9]+)')


class OtoDomSpider(scrapy.Spider):
    name = "otodom"

    def start_requests(self):
        yield scrapy.Request(url='https://otodom.pl/sprzedaz/mieszkanie/krakow/', callback=self.parse_page)

    def parse_page(self, response):
        links = response.css("header.offer-item-header h3 a::attr(href)").extract()

        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_property)

        next_link = response.css("ul.pager li a[data-dir*=next]::attr(href)").extract_first()

        if next_link:
            yield scrapy.Request(url=next_link, callback=self.parse_page)

    def parse_property(self, response):
        property_item = PropertyItem()
        sublist_keys = response.css("section.section-overview div ul li::text").extract()
        sublist_values = response.css("section.section-overview div ul li strong::text").extract()

        for key, value in zip(sublist_keys, sublist_values):
            property_item.set_field(normalize_string(key), normalize_string(value))

        property_item['url'] = response.url
        property_item['title'] = response.css("header h1::text").extract_first()
        property_item['price'] = extract_price(response)
        property_item['size'] = normalize_number(property_item['size'], type='float')
        property_item['price_per_sqm'] = property_item['price'] / property_item['size']
        property_item['location'] = extract_geo_data(response)
        property_item['images'] = extract_images(response)
        property_item['notified_on'] = None

        yield property_item


def extract_geo_data(response):
    scripts = response.css("div script::text").extract()
    latitude = 0.0
    longitude = 0.0

    for script in scripts:
        match = re.search(GEO_LOCATION_PATTERN, script)

        if match:
            latitude = match.group(1)
            longitude = match.group(2)
            break

    return {
        'lat': normalize_number(latitude, type='float'),
        'lon': normalize_number(longitude, type='float')
    }


def extract_images(response):
    return response.css("div.slick-track picture source::attr(srcset)").extract()


def extract_price(response):
    header_fields = response.css("header div div div::text").extract()

    for header_field in header_fields:
        if header_field.endswith(u"zł"):
            return normalize_number(header_field)
