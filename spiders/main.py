from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.spiders.otodom_spider import OtoDomSpider

process = CrawlerProcess(get_project_settings())

process.crawl(OtoDomSpider)
process.start()