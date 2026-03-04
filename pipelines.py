# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
import logging
import scrapy
from scrapy.exceptions import DropItem


class BmwScraperPipeline:
    def process_item(self, item, spider):
        return item


class DataValidationPipeline:
    """
    Pipeline for validating and cleaning scraped car items.

    Fulfills Bonus Task 6.2:
    - Validates required fields (model, name, registration).
    - Cleans and converts the mileage field to an integer.
    - Normalizes the fuel field to lowercase.
    """

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """
        Processes the item, validates required fields, and cleans data formats.

        :param item: The scraped item containing car details.
        :type item: scrapy.Item
        :param spider: The spider that scraped the item.
        :type spider: scrapy.Spider
        :raises DropItem: If any of the required fields are missing.
        :return: The cleaned item ready for the next pipeline.
        :rtype: scrapy.Item
        """
        required_fields = ['model', 'name', 'registration']
        for field in required_fields:
            if not item.get(field):
                spider.log(f"Missing required field '{field}'. Dropping item: {item}", level=logging.WARNING)
                raise DropItem(f"Missing required field: {field}")

        mileage = item.get('mileage')
        if mileage:
            try:
                clean_mileage = str(mileage).replace(',', '').replace('miles', '').strip()
                item['mileage'] = int(clean_mileage)
            except ValueError:
                spider.log(f"Could not convert mileage to int: {mileage}", level=logging.WARNING)
                item['mileage'] = None

        fuel = item.get('fuel')
        if fuel:
            item['fuel'] = str(fuel).lower()

        return item


class SQLitePipeline:
    """
    Pipeline for storing scraped car items into a SQLite database.
    """

    def open_spider(self, spider: scrapy.Spider) -> None:
        """
        Opens the database connection and creates the table if it does not exist
        when the spider is opened.

        :param spider: The spider that was opened.
        :type spider: scrapy.Spider
        :return: None
        :rtype: None
        """
        self.conn = sqlite3.connect('bmw_cars.db')
        self.curr = self.conn.cursor()
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS cars(
                registration TEXT PRIMARY KEY,
                model TEXT,
                name TEXT,
                mileage INTEGER,
                registered TEXT,
                engine TEXT,
                range TEXT,
                fuel TEXT,
                transmission TEXT,
                exterior TEXT,
                upholstery TEXT
            )
        """)

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """
        Inserts the scraped item into the database. Ignores duplicates based on
        the registration primary key.

        :param item: The scraped item to be stored.
        :type item: scrapy.Item
        :param spider: The spider that scraped the item.
        :type spider: scrapy.Spider
        :return: The item after database insertion.
        :rtype: scrapy.Item
        """
        self.curr.execute("""
            INSERT OR IGNORE INTO cars VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.get('registration'), item.get('model'), item.get('name'),
            item.get('mileage'), item.get('registered'), item.get('engine'),
            item.get('range'), item.get('fuel'), item.get('transmission'),
            item.get('exterior'), item.get('upholstery')
        ))
        self.conn.commit()
        return item

    def close_spider(self, spider: scrapy.Spider) -> None:
        """
        Closes the database connection when the spider finishes.

        :param spider: The spider that was closed.
        :type spider: scrapy.Spider
        :return: None
        :rtype: None
        """
        self.conn.close()
