__author__ = "roman.subik"

import requests
from spiders.settings import ELASTICSEARCH_INDEX, ELASTICSEARCH_PORT, ELASTICSEARCH_SERVERS, ELASTICSEARCH_TYPE

MAPPING = {
    "settings": {
        "number_of_shards": 1
    },
    "mappings": {
        ELASTICSEARCH_TYPE: {
            "dynamic_templates": [
                {
                    "location_field": {
                        "mapping": {
                            "type": "geo_point",
                            "tree": "quadtree",
                            "precision": "1m"
                        },
                        "match": "location"
                    }
                },
                {
                    "all_string_fields": {
                        "mapping": {
                            "type": "string",
                            "analyzer": "polish"
                        },
                        "match_mapping_type": "string"
                    }
                }]
        }
    }
}


class ElasticSearchHelper(object):
    def __init__(self):
        self.url = "{}:{}/{}/".format(ELASTICSEARCH_SERVERS[0], ELASTICSEARCH_PORT, ELASTICSEARCH_INDEX)

    def init_mappings(self, mapping):
        response = requests.delete(self.url)
        response = requests.put(self.url, json=mapping)
        pass
