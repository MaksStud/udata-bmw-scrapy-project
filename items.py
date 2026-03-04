# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BmwScraperItem(scrapy.Item):
    model = scrapy.Field()
    name = scrapy.Field()
    mileage = scrapy.Field()
    registered = scrapy.Field()
    engine = scrapy.Field()
    range = scrapy.Field()
    fuel = scrapy.Field()
    transmission = scrapy.Field()
    exterior = scrapy.Field()
    upholstery = scrapy.Field()
    registration = scrapy.Field()
