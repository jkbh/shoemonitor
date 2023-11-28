import scrapy
from shoemonitor.items import ShoeItem
from shoemonitor.loaders import ShoeLoader

class BasketballdirektSpider(scrapy.Spider):
    name = "basketballdirekt"
    allowed_domains = ["www.basketballdirekt.de"]
    start_urls = ["https://www.basketballdirekt.de/basketballschuhe"]

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
        loader = ShoeLoader(item=ShoeItem(), response=response) 

        loader.add_value("url", response.url)
        loader.add_css("name", "h1::text")
        loader.add_css("price", ".product-data span[itemprop='price']::text")
        loader.add_css("sizes", '.prodsizes__item:not([class*="notavail"])::text')
        loader.add_css("color", ".color::text")
        loader.add_xpath('height', "//label[contains(., 'Höhe:')]/../text()")
        
        return loader.load_item()

