__author__ = "roman.subik"

import scrapy

from datetime import datetime, timedelta
import re

from utils import normalize_number, normalize_string
from spiders.items import PropertyItem


class OtoDomSpider(scrapy.Spider):
    name = "otodom"

    def start_requests(self):
        yield scrapy.Request(url='https://otodom.pl/sprzedaz/mieszkanie/krakow/', callback=self.parse_page)

    def parse_page(self, response):
        links = response.css("header.offer-item-header h3 a::attr(href)").extract()

        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_property)

        next_link = response.css("ul.pager li a::attr(href)").extract_first()

        if next_link:
            yield scrapy.Request(url=next_link, callback=self.parse_page)

        # filename = 'links.txt'
        # with open(filename, 'wa') as f:
        #     f.write(str(links))
        # self.log('Saved file %s' % filename)

    def parse_property(self, response):
        property_item = PropertyItem()
        price, size, num_rooms, floor = response.css("ul.main-list li span strong::text").extract()
        sublist_keys = response.css("ul.sub-list li strong::text").extract()
        sublist_values = response.css("ul.sub-list li::text").extract()
        sublist = {}

        for i in range(0, len(sublist_keys)):
            sublist[normalize_string(sublist_keys[i])] = normalize_string(sublist_values[i])

        extras = response.css("ul.params-list li")

        extras_list = {}

        for index, extra in enumerate(extras):
            h4 = extra.css("h4::text").extract_first()

            if h4:
                extras_list[normalize_string(h4)] = normalize_string(
                    extra.css('ul.dotted-list li::text').extract_first()
                )

        latitude, longitude = extract_geo_data(response)

        property_item['title'] = response.css("header.col-md-offer-content h1::text").extract_first()
        property_item['price'] = normalize_number(price)
        property_item['size'] = normalize_number(size, type='float')
        property_item['num_rooms'] = normalize_number(num_rooms)
        property_item['floor'] = normalize_number(floor)
        property_item['price_per_sqm'] = normalize_number(price) / float(normalize_number(size))
        property_item['sublist'] = sublist
        property_item['extras_list'] = extras_list
        property_item['date_added'] = extract_date(response)
        property_item['latitude'] = latitude
        property_item['longitude'] = longitude

        yield property_item


def extract_date(response):
    date = response.css("div.text-details div.right p::text").extract_first()

    m = re.search('ponad ([0-9])+', date)

    if m:
        return datetime.now() - timedelta(days=int(m.group(1)))

    m = re.search('([0-9])+\.([0-9])+\.([0-9])+', date)

    if m:
        day, month, year = m.group(1, 2, 3)
        return datetime(day=int(day), month=int(month), year=int(year))

    return None


def extract_geo_data(response):
    latitude = response.css("div#adDetailInlineMap::attr(data-poi-lat)").extract_first()
    longitude = response.css("div#adDetailInlineMap::attr(data-poi-lon)").extract_first()

    return normalize_number(latitude, type='float'), normalize_number(longitude, type='float')
