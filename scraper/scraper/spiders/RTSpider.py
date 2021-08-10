import requests
import scraper.middlewares
import scraper.pipelines
import scraper.settings
from bs4 import BeautifulSoup as soup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scraper.spiders.baseSpider import BaseArticleSpider, API_URL, ARTICLES, SOURCES, COUNTRIES


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
        article["url"] = response.url
        article["title"] = response.css('h1::text').extract_first()
        article["text"] = soup(response.text, 'html.parser').get_text()
        article["length"] = len(article["text"])
        article["source"] = self.get_source_id('RT', 'www.rt.com', 'Russia')
        article["countries"] = [self.get_country_id('Russia')]

        res = requests.post(API_URL + ARTICLES, data=article)
        return article
