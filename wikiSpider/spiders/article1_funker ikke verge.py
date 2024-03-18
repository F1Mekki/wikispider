import scrapy
from wikiSpider.items import Article

class ArticleSpider(scrapy.Spider):
    name = 'article1'
    allowed_domains = 'theverge.com'
    start_link = 'https://www.theverge.com/reviews'

    def start_requests(self):
        #this is where you define how to perform the crawl

        urls = ['https://www.theverge.com/reviews']

        return [scrapy.Request(url=url, callback=self.parse) for url in urls]

    def parse(self, response):
        #this is where you define how to extract structured data from their pages (scraping items)
        article = Article()
        article['url'] = response.url
        article['title'] = response.xpath('//h1/text()').extract_first()
        lastUpdated = response.xpath("//*[@id='footer-info-lastmod']/text()").extract_first()
        article['lastUpdated'] = lastUpdated.replace('Last edited on ', '')
        yield article
        
        for href in response.xpath('//a/@href').getall():
            yield scrapy.Request(response.urljoin(href), self.parse)
