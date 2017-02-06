# -*- coding: utf-8 -*-

__author__ = "roman.subik"

import json
from datetime import datetime

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
        u'query_path': 'spiders/search/queries/west_krakow.json'
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
            query_body = {}
            with open(query['query_path']) as query_file:
                query_body = json.load(query_file)

            response = requests.get(self.url + '_search', json=query_body)

            if response.status_code == 200:
                results[query['title']] = response.json().get('hits', [])
            else:
                print('Got response {} form ElasticSearch, reason: {}'.format(response.status_code, response.json))

        return results

    def mark_as_notified(self, query_results):
        for query_title in query_results:
            result = query_results[query_title]

            if not result['total']:
                continue

            hits = result.get('hits', [])
            for hit in hits:
                update_url = '{}{}/{}/_update'.format(self.url, ELASTICSEARCH_TYPE, hit['_id'])
                requests.post(update_url, json={
                    "doc": {
                        "notified_on": str(datetime.utcnow())
                    }
                })
