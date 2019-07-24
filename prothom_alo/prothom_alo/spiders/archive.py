# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin


class ArchiveSpider(scrapy.Spider):
    name = 'archive'
    allowed_domains = ['prothomalo.com/']
    start_urls = ['https://prothomalo.com/archive/']

    def parse(self, response):
        years = [str(i) for i in range(2013, 2020)]
        months = [str(i) for i in range(1, 13)]
        dates = [str(i) for i in range(1, 32)]

        for y in years:
            for m in months:
                for d in dates:
                    dateUrl = y+"-"+m+"-"+d
                    datewise_archive_url = urljoin(response.url, dateUrl)

                    yield scrapy.Request(datewise_archive_url, callback=self.parse_archive)

                    for p in range(2, 100):
                        page_url = "?page="+str(p)
                        datewise_archive_page_url = urljoin(
                            datewise_archive_url, page_url)
                        yield scrapy.Request(datewise_archive_url, callback=self.parse_archive)

    def parse_archive(self, response):

        article_div = response.xpath('//div[@class="listing"]')
        if article_div:
            article_links = article_div.xpath(
                './/a[@class="link_overlay"]/@href').extract()
            yield{"links": article_links}
        else:
            print("No articles")
