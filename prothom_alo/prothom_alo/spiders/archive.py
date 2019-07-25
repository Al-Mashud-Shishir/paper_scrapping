# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
import os
import re
# Create crawled files (if not created)


def insert_data_to_file(data):
    crawled = 'prothom_alo2.txt'

    if not os.path.isfile(crawled):
        write_file(crawled, data)
    else:
        append_to_file(crawled, data)


# Create a new file
def write_file(path, data):
    f = open(path, 'w', encoding="utf-8")
    f.write(data)
    f.close()


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a', encoding="utf-8") as file:
        file.write(data)

        # first_url=urljoin(datewise_archive_url, "?edition=print")
        # for extra in self.extra_urls:
        #     first_url = urljoin(datewise_archive_url, extra)
        # # ?edition=print&page=
        # # ?edition=online
        # # ?edition=online&page=2


class ArchiveSpider(scrapy.Spider):
    name = 'archive'
    allowed_domains = ['prothomalo.com/']
    start_urls = ['https://prothomalo.com/archive/']
    base_url = "https://prothomalo.com/"
    extra_urls = ["?edition=print", "?edition=online"]
    # website_possible_httpstatus_list = [403]
    # handle_httpstatus_list = [403]

    def parse(self, response):
        # os.remove("prothom_alo.txt")
        years = [str(i) for i in range(2013, 2020)]
        months = [str(i) for i in range(1, 13)]
        dates = [str(i) for i in range(1, 32)]

        for y in years:
            for m in months:
                for d in dates:
                    dateUrl = y+"-"+m+"-"+d
                    datewise_archive_url = urljoin(response.url, dateUrl)
                    for p in range(2, 12):
                        page_url = "?edition=print&page="+str(p)
                        datewise_archive_page_url = urljoin(
                            datewise_archive_url, page_url)
                        yield scrapy.Request(datewise_archive_page_url, callback=self.parse_archive, dont_filter=True)
                    # yield scrapy.Request(first_url, callback=self.parse_archive, dont_filter=True)

    def parse_archive(self, response):
        if response.status != 404:
            article_div = response.xpath('//div[@class="listing"]')
            if article_div:
                article_links = article_div.xpath(
                    './/a[@class="link_overlay"]/@href').extract()
                for article in article_links:
                    link = urljoin(self.base_url, article)
                    yield scrapy.Request(link, callback=self.parse_article, dont_filter=True)
            else:
                print("No articles")
                return

    def parse_article(self, response):
        # yield{"Url": response.url}
        bn_ps = response.xpath(
            "//div[@itemprop='articleBody']//p/text()").extract()
        for p in bn_ps:
            p = re.sub(
                '[A-Za-z0-9.@_=#$%^&*()<>/"\'‘’,\\}{~:১২৩৪৫৬৭৮৯০]+', ' ', p)
            p = re.sub('-', ' ', p)
            insert_data_to_file(p)
        # yield {"Text":bn_strings}
