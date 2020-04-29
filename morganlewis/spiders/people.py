# -*- coding: utf-8 -*-
from math import ceil
from datetime import datetime

import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest

from ..items import MorganlewisItem


class PeopleSpider(scrapy.Spider):
    name = 'people'
    allowed_domains = ['morganlewis.com']
    start_urls = ['https://www.morganlewis.com/our-people/']
    script_load_publist = """
    function main(splash)
      local url = splash.args.url
      assert(splash:go(url))
      assert(splash:wait(1))
    
      splash:runjs('document.getElementById("publist").click()')
      assert(splash:wait(3))
      splash:runjs('document.getElementById("pubviewmoreless").click()')
      assert(splash:wait(3))
      
      return {
        html = splash:html()
      }
    end   
    """

    def start_requests(self):
        yield SplashRequest('https://www.morganlewis.com/our-people/',
                            self.parse,
                            args={'wait': 5})

    def parse(self, response):

        people_total = int(response.xpath('//*[@class="c-results__total"]/span/text()').re(r'\((\d+)\)')[0])
        num_per_page = 100

        for page in range(1, ceil(people_total / num_per_page) + 1):
            url_api = (
                f'https://www.morganlewis.com/api/sitecore/searchredesign/peopleresultslisting?'
                f'keyword=&category=bb82d24a9d7a45bd938533994c4e775a&sortBy=lastname&pageNum={page}'
                f'&numberPerPage={num_per_page}&numberPerSection=5&enforceLanguage=&language'
                f'ToEnforce=&school=&position=&location=&court=&judge=&isFacetRefresh=false'
            )
            yield Request(url_api, self.get_next_page)

    def get_next_page(self, response):
        profile_urls = response.xpath('//*[@class="c-content_team__card-info"]/a/@href').extract()
        for url in profile_urls:
            yield SplashRequest(response.urljoin(url),
                                self.parse_item,
                                endpoint='execute',
                                args={
                                    'lua_source': self.script_load_publist,
                                    'wait': 2.5
                                }
            )

    def parse_item(self, response):
        item = MorganlewisItem()

        item['url'] = response.url

        item['photo_url'] = \
            response.urljoin(response.xpath('//*[@class="thumbnail"]/img/@src').get())

        item['fullname'] = \
            response.xpath('//*[@class="person-heading"]//span/text()').get()

        item['position'] = \
            response.xpath('//*[@class="person-heading"]/h2/text()').get().strip()

        item['phone_numbers'] = \
            response.xpath('//*[@class="underline"]/a/text()').extract()

        item['email'] = \
            response.xpath('//p[@class="bio-mail-id"]/a/text()').get().strip()

        item['services'] = \
            response.xpath('//h2[text()="Services"]/following-sibling::ul/li/a/text()').extract()

        item['sectors'] = \
            response.xpath('//h2[text()="Sectors"]/following-sibling::ul/li/a/text()').extract()

        item['publications'] = [
            f"{publist.xpath('span/text()').get()} - {publist.xpath('text()').get().lstrip(' -')}"
            for publist
            in response.xpath('//div[@class="hidden-cont" or @id="pubexpandlist"]/p/a[not(@data-show)]')
        ]

        item['person_brief'] = \
            response.xpath('//p[@class="heading-brief"]/text()').get().strip().replace('\n', '')

        item['datetime_scrapped'] = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        yield item
