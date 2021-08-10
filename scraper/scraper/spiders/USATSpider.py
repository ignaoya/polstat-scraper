import requests
import scraper.middlewares
import scraper.pipelines
import scraper.settings
from bs4 import BeautifulSoup as soup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scraper.spiders.baseSpider import BaseArticleSpider, API_URL, ARTICLES, SOURCES, COUNTRIES


class USATArticleSpider(BaseArticleSpider):
    name = 'USATarticle'
    allowed_domains = ['eu.usatoday.com']
    start_urls = ['https://eu.usatoday.com/news/world/']
    rules = [
        Rule(LinkExtractor(allow='(/story/).*'),
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
        article["source"] = self.get_source_id('USA Today', 'www.usatoday.com', 'United States')
        article["countries"] = [self.get_country_id('United States')]

        res = requests.post(API_URL + ARTICLES, data=article)
        return article

