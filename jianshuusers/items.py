# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field,Item


class UserItem(Item):
    url = Field()
    nickname = Field()
    atten = Field()
    fans = Field()
    articles = Field()
    collections = Field()
    words = Field()
    likes = Field()
