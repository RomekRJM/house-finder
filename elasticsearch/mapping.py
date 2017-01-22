# -*- coding: utf-8 -*-

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

QUERIES = [
    {
        u'title': u'Kraków zachód',
        u'query_path': 'elasticsearch/queries/west_krakow.json'
    }
]


class ElasticSearchHelper(object):
    def __init__(self):
        self.url = "{}:{}/{}/".format(ELASTICSEARCH_SERVERS[0], ELASTICSEARCH_PORT, ELASTICSEARCH_INDEX)

    def redo_index(self, mapping):
        requests.delete(self.url)
        requests.put(self.url, json=mapping)

    def find_interesting_flats(self):
        results = {}

        for query in QUERIES:
            response = requests.get(self.url + '_search', query)

            if response.code == 200:
                results[query['title']] = response.json.get('hits', [])

            print('Got response {} form ElasticSearch, reason: {}'.format(response.code, response.json))

        return results
