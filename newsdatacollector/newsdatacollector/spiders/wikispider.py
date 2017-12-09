# -*- coding: utf-8 -*-
import scrapy
from scrapy.cmdline import execute

class WikispiderSpider(scrapy.Spider):
    name = 'wikispider'
    siteroot='https://en.wikipedia.org'
    #allowed_domains = ['https://en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_newspapers_in_India_by_circulation']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        print(response.url)
        newssitesurl = response.css('table.wikitable').xpath('//td/i//a/@href').extract()
        for url in newssitesurl:
            yield scrapy.Request(self.siteroot + url, callback=self.parse_newspage)

    def parse_newspage(self, response):
        url = response.css('table.infobox').xpath(
            "//*[contains(text(),'Website')]/following-sibling::*//a/@href").extract_first()
        if url != None:
            yield scrapy.Request(url, callback=self.parse_newssite)

        else:
            print("not found website for {}".format(response.url))

    def parse_newssite(self, response):
        print(response.url)

        with open('../most_popular_site_analysis.csv', 'a') as resultfile:
            resultfile.write('{},{},{},{}\n'.format(response.url, len(response.text), len(response.xpath('//a')),
                                                    self.get_all_images(response)))
        print('done for{}'.format(response.url))

    def get_all_images(self, response):
        input_image = len(response.xpath("//input[@type='image']"))
        url_im = len(response.xpath('//img'))
        class_img = len(response.xpath("//*[starts-with(@class,'img')]"))
        total = url_im + input_image + class_img
        return total

execute('scrapy crawl wikispider'.split())
