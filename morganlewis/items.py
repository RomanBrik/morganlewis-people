# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import six
import json
from collections import OrderedDict

from scrapy import Item, Field


class OrderedItem(Item):
    def __init__(self, *args, **kwargs):
        self._values = OrderedDict()
        if args or kwargs:
            for k, v in six.iteritems(dict(*args, **kwargs)):
                self[k] = v

    def __repr__(self):
        return json.dumps(OrderedDict(self), ensure_ascii = False)


class PeopleItem(OrderedItem):
    # define the fields for your item here like:
    url = Field()
    photo_url = Field()
    fullname = Field()
    position = Field()
    phone_numbers = Field()
    email = Field()
    services = Field()
    sectors = Field()
    publications = Field()
    person_brief = Field()
    datetime_scrapped = Field()
