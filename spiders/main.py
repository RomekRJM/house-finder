# -*- coding: utf-8 -*-

import os
import sys

from notifier.sender import EmailSender
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from search.elasticsearch_helper import ElasticSearchHelper, MAPPING
from spiders.spiders.otodom_spider import OtoDomSpider

mode = sys.argv[1]

if __name__ == '__main__':

    es_helper = ElasticSearchHelper()

    if mode == 'init':
        es_helper.redo_index(MAPPING)

    elif mode == 'crawl':
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'spiders.settings'
        process = CrawlerProcess(get_project_settings())
        process.crawl(OtoDomSpider)
        process.start()

    else:
        query_results = es_helper.find_interesting_flats()
        sender = EmailSender()
        sender.send_email(['romek.rjm@gmail.com', 'dorota.kf.s@gmail.com'],
                          "New cool flats available in Krakow!",
                          query_results
                          )
        es_helper.mark_as_notified(query_results)
