import scrapy
from items import BmwCarItem


class BmwSpider(scrapy.Spider):
    name = "bmw_uk"
    allowed_domains = ["usedcars.bmw.co.uk"]
    start_urls = ["https://usedcars.bmw.co.uk/result/?payment type=cash&size=23&source=home"]

    page_count = 1

    def parse(self, response):
        car_links = response.css('a.uvl-car-card__link::attr(href)').getall()
        for link in car_links:
            yield response.follow(link, callback=self.parse_detail)

        if self.page_count < 5:
            next_page = response.css('a.uvl-pagination__next::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        item = BmwCarItem()

        item['model'] = response.css('.uvl-car-details__model::text').get(default='').strip()
        item['name'] = response.css('.uvl-car-details__name::text').get(default='').strip()

        specs = {}
        spec_elements = response.css('.uvl-car-details__spec-list-item')

        for spec in spec_elements:
            label = spec.css('.uvl-car-details__spec-label::text').get(default='').lower().strip()
            value = spec.css('.uvl-car-details__spec-value::text').get(default='').strip()
            specs[label] = value

        item['mileage'] = specs.get('mileage')
        item['registered'] = specs.get('registered')
        item['engine'] = specs.get('engine')
        item['range'] = specs.get('range')
        item['fuel'] = specs.get('fuel')
        item['transmission'] = specs.get('transmission')
        item['exterior'] = specs.get('exterior')
        item['upholstery'] = specs.get('upholstery')
        item['registration'] = specs.get('registration')

        yield item
