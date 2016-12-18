__author__ = "roman.subik"

import scrapy

from utils import normalize_number, normalize_string


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

        yield {
            'title': response.css("header.col-md-offer-content h1::text").extract_first(),
            'price': normalize_number(price),
            'size': normalize_number(size),
            'num_rooms': normalize_number(num_rooms),
            'floor': normalize_number(floor),
            'price_per_sqm': normalize_number(price) / float(normalize_number(size)),
            'sublist': sublist,
            'extras_list': extras_list
        }