
# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class WinesSpider(CrawlSpider):
    name = 'wines'
    allowed_domains = ['www.winemag.com']
    # start_urls = ['https://www.winemag.com/?s=&drink_type=wine&page=230']
    start_urls = ['https://www.winemag.com/?s=&drink_type=wine&page={}&search_type=reviews'.format(x) for x in range(2610, 2700)]
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@class="review-listing row"]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pagination"]/ul/li/a'))
    )
    
    def parse_item(self, response):
        yield{
            'title': response.xpath('//div[@class="article-title"]/h1/text()').get(),
            'rating_points': response.xpath('//h1/span[@class="rating"]/text()').get(),
            'description': response.xpath('//p[@class="description"]/text()').get(),
            'taster_name': response.xpath('//span[@class="taster-area"]/a/text()').get(),
            #'price': response.xpath('(//div[@class="info medium-9 columns"]/span)[1]/span/text()').get().split(',')[0],
            'price': response.xpath('(//div[@class="info medium-9 columns"]/span)[1]/span/text()').get(),
            'designation': response.xpath('(//div[@class="info medium-9 columns"]/span)[2]/span/text()').get(),
            'variety': response.xpath('//div[@class="info medium-9 columns"]/span/a/text()').getall()[0],
            'appellation': response.xpath('//div[@class="info medium-9 columns"]/span/a/text()').getall()[1],
            #'state': response.xpath('//div[@class="info medium-9 columns"]/span/a/text()').getall()[3],
            'country':response.xpath('//div[@class="info medium-9 columns"]/span/a/text()').getall()[-1],
            'winery': response.xpath('//div[@class="info medium-9 columns"]/span/span/a/text()').getall()[1],
            'alcohol': response.xpath('//div[@class="info small-9 columns"]/span/span/text()').getall()[0],
            'bottle_size': response.xpath('//div[@class="info small-9 columns"]/span/span/text()').getall()[1],
            'category': response.xpath('//div[@class="info small-9 columns"]/span/span/text()').getall()[2]
            }