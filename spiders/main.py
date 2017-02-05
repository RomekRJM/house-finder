# -*- coding: utf-8 -*-

import os
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from notifier.sender import EmailSender
from search.elasticsearch_helper import ElasticSearchHelper, MAPPING
from spiders.spiders.otodom_spider import OtoDomSpider

mode = sys.argv[1]

if __name__ == '__main__':

    es_helper = ElasticSearchHelper()

    if mode == 'crawl':
        es_helper.redo_index(MAPPING)

    elif mode == 'crawl':
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'spiders.settings'
        process = CrawlerProcess(get_project_settings())
        process.crawl(OtoDomSpider)
        process.start()

    else:
        sender = EmailSender()
        sender.send_email(['romek.rjm@gmail.com', 'sabina.subik@gmail.com'],
                          "New cool flats available in Krakow!",
                          es_helper.find_interesting_flats()
                          )
