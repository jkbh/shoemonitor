import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity
from shoemonitor.items import ShoeItem

class BasketballdirektSpider(scrapy.Spider):
    name = "basketballdirekt"
    allowed_domains = ["www.basketballdirekt.de"]
    start_urls = ["https://www.basketballdirekt.de/basketballschuhe?sort=best&category=basketballschuhe"]

    def parse(self, response):
        page_urls = response.css("a.page-link::attr(href)").getall()
        for url in set(page_urls):
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        cards = response.css(".productcard")
        shoe_urls = cards.css(".productcard__overlay > a::attr(href)").getall()

        for url in shoe_urls[:2]:
            yield scrapy.Request(url, callback=self.parse_shoe)       
    

    def parse_shoe(self, response):
        loader = ItemLoader(item=ShoeItem(), response=response)

        loader.default_output_processor = TakeFirst()
        loader.default_input_processor = MapCompose(str.strip)

        loader.price_in = MapCompose(
            lambda x: float(x.replace(",", "."))
        )

        loader.sizes_in = MapCompose(str.strip)
        loader.sizes_out = Identity()
        
        loader.add_value("url", response.url)
        loader.add_css("name", ".product-data h1::text")
        loader.add_css("price", ".product-data .price--actual span[itemprop='price']::text")
        loader.add_css("sizes", '.product-data ul.prodsizes > li:not([class*="notavail"])::text')
        loader.add_css("color", ".product-data .color::text")
        loader.add_xpath('height', "//label[contains(., 'Höhe:')]/../text()")
        
        return loader.load_item()

