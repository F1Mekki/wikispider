import scrapy
from wikiSpider.items import Article
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

# command
# scrapy runspider C:\Users\flipp\Documents\LOCAL_PROJECTS\INFO215L\wikiSpider\wikiSpider\spiders\article1.py -o reviews.csv


class ArticleSpider(scrapy.Spider):
    name = 'article1'
    allowed_domains = ['theverge.com']

    rules = [
        Rule(LinkExtractor(allow=r'^(https://www.theverge.com/)((?!:).)*$'),
            callback='parse_items', follow=True, cb_kwargs={'is_article' : True}),
        Rule(LinkExtractor(allow=r'.*'),
            callback='parse_items', cb_kwargs={'is_article' : False}),
    ]
    
    def start_requests(self):
        #this is where you define how to perform the crawl

        urls = ['https://www.theverge.com/reviews']

        return [scrapy.Request(url=url, callback=self.parse) for url in urls]

    def parse(self, response):
        #this is where you define how to extract structured data from their pages (scraping items)
        article = Article()
        article['url'] = response.url
        article['title'] = response.xpath('//h1/text()').get()
        article['author_name'] = response.xpath('//a[@href="/authors"]/text()').get()
        article['author_profile'] = response.xpath('//span[@class="c-byline__item"]/a/@href').get()
           
        
        yield article
        

        for href in response.xpath('//a/@href').getall():
            yield scrapy.Request(response.urljoin(href), self.parse)
        
