import requests
import scraper.middlewares
import scraper.pipelines
import scraper.settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

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

        data = { "url": url, "name": name, "origin": self.get_country(country) }
        res = requests.post(API_URL + SOURCES, data=data)
        source_id = res.json()[0]['id']
        return source_id

    def get_country_id(self, name: str) -> int:
        res = requests.get(API_URL + COUNTRIES)
        for item in res.json():
            if item['name'] == name:
                country_id = int(item['id'])
                return country_id

        data = { "name": name }
        res = requests.post(API_URL + SOURCES, data=data)
        country_id = res.json()[0]['id']
        return country_id


class RTArticleSpider(BaseArticleSpider):
    name = 'RTarticle'
    allowed_domains = ['www.rt.com']
    start_urls = ['https://www.rt.com']
    rules = [
        Rule(LinkExtractor(allow='(/op-ed/).*'),
            callback='parse_items', follow=True),
    ]

    # Page count limit to avoid over-scraping and getting banned while in development
    COUNT_MAX = 5
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': COUNT_MAX
    }

    def parse_items(self, response):
        article = {}
        divs = response.xpath('//div')
        article["url"] = response.url
        article["title"] = response.css('h1::text').extract_first()
        article["text"] = ''.join(divs.xpath('.//p').extract())
        article["length"] = len(article["text"])
        article["source"] = self.get_source_id('RT', 'www.rt.com', 'Russia')
        article["countries"] = [self.get_country_id('Russia')]

        res = requests.post(API_URL + ARTICLES, data=article)
        return article

