# -*- coding: utf-8 -*-

import sys

from scrapy.crawler import CrawlerProcess
# from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from spiders.spiders.otodom_spider import OtoDomSpider
from elasticsearch.mapping import ElasticSearchHelper, MAPPING
from notifier.sender import EmailSender

mode = sys.argv[1]

if __name__ == '__main__':

    if mode == 'init':
        es_helper = ElasticSearchHelper()
        es_helper.redo_index(MAPPING)

        # settings = Settings()
        # os.environ['SCRAPY_SETTINGS_MODULE'] = 'spiders.settings'
        # settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
        # settings.setmodule(settings_module_path, priority='project')

        process = CrawlerProcess(get_project_settings())
        process.crawl(OtoDomSpider)
        process.start()

    else:
        sender = EmailSender()
        sender.send_email(['romek.rjm@gmail.com', 'sabina.subik@gmail.com'],
                          "New cool flats available in Krakow!",
                          "Here is the full list: EMPTY_FOR_NOW"
                          )
