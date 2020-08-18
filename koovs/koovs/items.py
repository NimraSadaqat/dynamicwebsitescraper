# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KoovsItem(scrapy.Item):

    no = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    pass
