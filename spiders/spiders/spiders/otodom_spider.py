__author__ = "roman.subik"

import re
from datetime import datetime, timedelta

import scrapy
from spiders.items import PropertyItem

from utils import normalize_number, normalize_string


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
        price, size, num_rooms, floor = response.css("ul.main-list li span strong::text").extract()
        sublist_keys = response.css("ul.sub-list li strong::text").extract()
        sublist_values = response.css("ul.sub-list li::text").extract()

        for i in range(0, len(sublist_keys)):
            property_item.set_field(normalize_string(sublist_keys[i]), normalize_string(sublist_values[i]))

        extras = response.css("ul.params-list li")

        for index, extra in enumerate(extras):
            h4 = extra.css("h4::text").extract_first()

            if h4:
                property_item.set_field(normalize_string(h4), normalize_string(
                    extra.css('ul.dotted-list li::text').extract_first()
                ))

        property_item['url'] = response.url
        property_item['title'] = response.css("header.col-md-offer-content h1::text").extract_first()
        property_item['price'] = normalize_number(price)
        property_item['size'] = normalize_number(size, type='float')
        property_item['num_rooms'] = normalize_number(num_rooms)
        property_item['floor'] = normalize_number(floor)
        property_item['price_per_sqm'] = normalize_number(price) / float(normalize_number(size))
        property_item['date_added'] = extract_date(response)
        property_item['location'] = extract_geo_data(response)

        yield property_item


def extract_date(response):
    date = response.css("div.text-details div.right p::text").extract_first()

    m = re.search('ponad ([0-9]+)', date)

    if m:
        return datetime.now() - timedelta(days=int(m.group(1)))

    m = re.search('([0-9]+)\.([0-9]+)\.([0-9]+)', date)

    if m:
        day, month, year = m.group(1, 2, 3)
        return datetime(day=int(day), month=int(month), year=int(year))

    return None


def extract_geo_data(response):
    latitude = response.css("div#adDetailInlineMap::attr(data-poi-lat)").extract_first()
    longitude = response.css("div#adDetailInlineMap::attr(data-poi-lon)").extract_first()

    return {
        'lat': normalize_number(latitude, type='float'),
        'lon': normalize_number(longitude, type='float')
    }
