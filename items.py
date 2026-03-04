# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BmwCarItem(scrapy.Item):
    """
    Scrapy Item for storing collected data about BMW cars.

    This class defines the data structure extracted from the detailed
    specifications page (Detail Page) of each car listing.
    All fields comply with the requirements of the technical task.
    """
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
