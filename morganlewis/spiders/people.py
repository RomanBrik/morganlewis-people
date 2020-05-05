# -*- coding: utf-8 -*-
from string import Template
from datetime import datetime

import scrapy
import requests

from ..items import PeopleItem


class People2Spider(scrapy.Spider):
    name = 'people'

    def __init__(self, *args, **kwargs):
        self.items_per_page = 100
        self.page = 1
        self.url_api = Template(
            'https://www.morganlewis.com/api/sitecore/searchredesign/peopleresultslisting?'
            'keyword=&category=bb82d24a9d7a45bd938533994c4e775a&sortBy=lastname&pageNum=$page'
            '&numberPerPage=$items_per_page&numberPerSection=5&enforceLanguage=&language'
            'ToEnforce=&school=&position=&location=&court=&judge=&isFacetRefresh=false'
        )
        self.pub_url = 'https://www.morganlewis.com/api/sitecore/accordion/getaccordionlist'
        super().__init__(*args, **kwargs)

    def start_requests(self):

        yield scrapy.Request(
            self.url_api.substitute(page=self.page, items_per_page=self.items_per_page),
            callback=self.parse
        )
        self.page += 1

    def parse(self, response):
        urls = response.xpath('//*[@class="c-content_team__card-info"]/a/@href').getall()

        for url in urls:
            yield response.follow(url, callback=self.parse_item)

        if len(urls) == self.items_per_page:
            yield scrapy.Request(
                self.url_api.substitute(page=self.page, items_per_page=self.items_per_page),
                callback=self.parse
            )
            self.page += 1

    def parse_item(self, response):
        item = PeopleItem()

        item['url'] = response.url

        item['photo_url'] = \
            response.urljoin(response.xpath('//*[@class="thumbnail"]/img/@src').get())

        item['fullname'] = \
            response.xpath('//*[@class="person-heading"]//span/text()').get()

        item['position'] = \
            response.xpath('//*[@class="person-heading"]/h2/text()').get()

        item['phone_numbers'] = \
            response.xpath('//*[@class="underline"]/a/text()').getall()

        item['email'] = \
            response.xpath('//p[@class="bio-mail-id"]/a/text()').get()

        item['services'] = \
            response.xpath('//h2[text()="Services"]/following-sibling::ul/li/a/text()').getall()

        item['sectors'] = \
            response.xpath('//h2[text()="Sectors"]/following-sibling::ul/li/a/text()').getall()

        pub_response = requests.post(self.pub_url,
                                     json={
                                         "itemID": response.xpath('//script').re(r'itemID: "({.+})')[0],
                                         "itemType": "publicationitemlist",
                                         "printView": ""
                                     }
                                     )
        selector = scrapy.selector.Selector(text=pub_response.text)

        item['publications'] = [
            f'{sel.xpath("span/text()").get()}{sel.xpath("text()").get()}'.replace('\n', '')
            for sel
            in selector.xpath('//a[not(@class="more")]')
        ]

        item['person_brief'] = response.xpath('//p[@class="heading-brief"]/text()').get()

        item['datetime_scrapped'] = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

        yield item
