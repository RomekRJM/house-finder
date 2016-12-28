from scrapy.crawler import CrawlerProcess
# from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from spiders.spiders.otodom_spider import OtoDomSpider
from elasticsearch.mapping import ElasticSearchHelper, MAPPING

if __name__ == '__main__':
    es_helper = ElasticSearchHelper()
    es_helper.init_mappings(MAPPING)

    # settings = Settings()
    # os.environ['SCRAPY_SETTINGS_MODULE'] = 'spiders.settings'
    # settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    # settings.setmodule(settings_module_path, priority='project')

    process = CrawlerProcess(get_project_settings())
    process.crawl(OtoDomSpider)
    process.start()
