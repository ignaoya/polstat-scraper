import requests
from scrapy.spiders import CrawlSpider

API_URL = 'http://localhost:8000/api/'
ARTICLES = 'articles/'
SOURCES = 'sources/'
COUNTRIES = 'countries/'


class BaseArticleSpider(CrawlSpider):

    def get_source_id(self, name: str, url: str, country: str) -> int:
        res = requests.get(API_URL + SOURCES)
        for item in res.json():
            if item['name'] == name:
                source_id = int(item['id'])
                return source_id

        data = { "url": url, "name": name, "origin": self.get_country_id(country) }
        res = requests.post(API_URL + SOURCES, data=data)
        source_id = res.json()['id']
        return source_id

    def get_country_id(self, name: str) -> int:
        res = requests.get(API_URL + COUNTRIES)
        for item in res.json():
            if item['name'] == name:
                country_id = int(item['id'])
                return country_id

        data = { "name": name }
        res = requests.post(API_URL + COUNTRIES, data=data)
        country_id = res.json()['id']
        return country_id


