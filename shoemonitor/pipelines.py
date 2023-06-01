# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter
import os

class ShoemonitorPipeline:
    def __init__(self) -> None:
        self.exporter = None

    def open_spider(self, spider):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        project_dir = os.path.split(current_dir)[0]
        items_path = os.path.join(project_dir, 'web', 'items.json')

        self.file = open(items_path, 'wb')
        self.exporter = JsonLinesItemExporter(self.file)

    def close_spider(self, spider):
        self.file.close()
        
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    
