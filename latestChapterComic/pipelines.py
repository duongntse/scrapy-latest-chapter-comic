# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os


class LatestchaptercomicPipeline:
    def process_item(self, item, spider):
        return item


class JsonPipeline(object):
    my_items = []
    fileData = 'items.json'
    f = open('items.json', 'w').write('[]')

    def open_spider(self, spider):
        # read data from 'items.json', ex: data = [{...}, {...}]
        if os.path.exists(self.fileData):
            f = open(self.fileData, 'r')
            data = f.read()
            if data:
                items = json.loads(data)
                if items and len(items) > 0:
                    self.my_items = items
            f.close()

    def close_spider(self, spider):
        # write data to items.json
        f = open('items.json', 'w')

        f.write(json.dumps(self.my_items))
        f.write("\n")
        f.close()

    def process_item(self, item, spider):
        item.setdefault('website_name', '')
        item.setdefault('website_url', '')
        item.setdefault('comic_name', '')
        item.setdefault('comic_url', '')
        item.setdefault('cover_img', '')
        item.setdefault('main_chapters', [])
        item.setdefault('duck_chapters', [])
        item.setdefault('rock_chapters', [])
        item.setdefault('fox_chapters', [])
        item.setdefault('panda_chapters', [])

        self.my_items.append(dict(item))
