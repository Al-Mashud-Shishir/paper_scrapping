# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin


class ArchiveSpider(scrapy.Spider):
    name = 'archive'
    allowed_domains = ['prothomalo.com/']
    start_urls = ['https://prothomalo.com/archive/']

    def parse(self, response):
        article_div = response.xpath('//div[@class="listing"]')
        if article_div:
            article_links = article_div.xpath(
                './/a[@class="link_overlay"]/@href').extract()
            yield{"links": article_links}
        else:
            print("No articles")
