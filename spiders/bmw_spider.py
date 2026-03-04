import scrapy
from scrapy.http import Response
from scrapy_playwright.page import PageMethod
from typing import Generator, List, Dict, Any
from ..items import BmwCarItem


class BmwSpider(scrapy.Spider):
    """
    Spider for scraping BMW Approved Used Cars listings using Playwright.

    Navigates through search result pages, extracts car links, and
    fetches detailed specifications for each vehicle.
    """
    name = "bmw_uk"
    allowed_domains = ["usedcars.bmw.co.uk"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initializes the spider and sets the starting page count."""
        super().__init__(*args, **kwargs)
        self.page_count = 1
        self.max_pages = 5

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        """
        Generates the initial request to the search results page.

        :return: A generator yielding the initial Scrapy Request with Playwright metadata.
        :rtype: Generator[scrapy.Request, None, None]
        """
        url = "https://usedcars.bmw.co.uk/result/?payment_type=cash&size=23&source=home"

        yield scrapy.Request(
            url,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "a.uvl-c-advert__media-link"),
                ],
            },
            callback=self.parse
        )

    def parse(self, response: Response) -> Generator[scrapy.Request, None, None]:
        """
        Parses the search results page, yields requests for detail pages,
        and handles pagination logic.

        :param response: The HTTP response from the search results page.
        :type response: scrapy.http.Response
        :return: A generator yielding requests for car details and the next listing page.
        :rtype: Generator[scrapy.Request, None, None]
        """
        unique_links = self._extract_unique_links(response)

        for link in unique_links:
            yield response.follow(
                link,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "div.uvl-c-specification-overview__title")
                    ]
                },
                callback=self.parse_detail
            )

        if self.page_count < self.max_pages:
            self.page_count += 1
            next_page_url = f"https://usedcars.bmw.co.uk/result/?payment_type=cash&size=23&source=home&page={self.page_count}"

            yield scrapy.Request(
                next_page_url,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "a.uvl-c-advert__media-link"),
                    ]
                }
            )

    def parse_detail(self, response: Response) -> Generator[BmwCarItem, None, None]:
        """
        Parses the detailed car page to extract all necessary specifications.

        :param response: The HTTP response of the car detail page.
        :type response: scrapy.http.Response
        :return: A generator yielding the populated BmwCarItem.
        :rtype: Generator[BmwCarItem, None, None]
        """
        item = BmwCarItem()

        item['model'] = response.xpath('//h1//text()').get(default='').strip()
        item['name'] = response.xpath('//h2//text()').get(default='').strip()

        specs = self._extract_specifications(response)

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

    def _extract_unique_links(self, response: Response) -> List[str]:
        """
        Extracts and deduplicates car detail URLs from the listing page.

        :param response: The HTTP response containing car listings.
        :type response: scrapy.http.Response
        :return: A list of unique relative or absolute URLs.
        :rtype: List[str]
        """
        car_links = response.css('a.uvl-c-advert__media-link::attr(href)').getall()
        return list(set(car_links))

    def _extract_specifications(self, response: Response) -> Dict[str, str]:
        """
        Extracts vehicle specifications from the DOM into a key-value mapping.

        :param response: The HTTP response of the car detail page.
        :type response: scrapy.http.Response
        :return: A dictionary mapping specification labels to their values.
        :rtype: Dict[str, str]
        """
        specs = {}
        spec_blocks = response.xpath('//div[contains(@class, "uvl-c-specification-overview__title")]')

        for block in spec_blocks:
            label = block.xpath('.//span/text()').get(default='').lower().strip()
            value = block.xpath('following-sibling::div[contains(@class, "uvl-c-specification-overview__value")]/text()').get(default='').strip()
            if label:
                specs[label] = value

        return specs
