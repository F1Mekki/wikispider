import scrapy
from wikiSpider.items import Article

class ArticleSpider(scrapy.Spider):
    name = 'article1'
    allowed_domains = ['en.wikipedia.org']

    def start_requests(self):
        #this is where you define how to perform the crawl

        urls = ['https://en.wikipedia.org/wiki/Monty_Python']

        return [scrapy.Request(url=url, callback=self.parse) for url in urls]

    def parse(self, response):
        #this is where you define how to extract structured data from their pages (scraping items)
        article = Article()
        article['url'] = response.url
        article['title'] = response.xpath('//h1/text()').extract_first()
        lastUpdated = response.xpath("//*[@id='footer-info-lastmod']/text()").extract_first()
        article['lastUpdated'] = lastUpdated.replace('This page was last edited on ', '')
        yield article

        for href in response.xpath('//a/@href').getall():
            yield scrapy.Request(response.urljoin(href), self.parse)
        
