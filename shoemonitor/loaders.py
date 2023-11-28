from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join

class ShoeLoader(ItemLoader):
        default_input_processor = MapCompose(str.strip)

        price_in = MapCompose(
            lambda x: float(x.replace(",", "."))
        )

        sizes_in = MapCompose(str.strip)

 
