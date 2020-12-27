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
        self.my_items.sort(key=lambda x: x['raw_time'], reverse=True)
        f.write(json.dumps(self.my_items))
        f.write("\n")
        f.close()

    def process_item(self, item, spider):
        item.setdefault('comic_name', '')
        item.setdefault('raw_time', '')
        item.setdefault('cover_img', '')
        item.setdefault('chapter_title', '')
        item.setdefault('comic_url', '')
        item.setdefault('base_site_name', '')
        item.setdefault('base_site_url', '')
        item.setdefault('prev_chap', '')
        # print(f'process_item: {item}')
        self.my_items.append(dict(item))
        return item


class JsonPipelineVer2(object):
    my_comics = []
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
                    self.my_comics = items
            f.close()

    def close_spider(self, spider):
        # write data to items.json
        f = open('items.json', 'w')
        self.my_comics.sort(key=lambda x: x['raw_time'], reverse=True)
        f.write(json.dumps(self.my_comics))
        f.write("\n")
        f.close()

    def process_item(self, item, spider):

        item.setdefault('website_name', '')
        item.setdefault('website_url', '')
        item.setdefault('comic_name', '')
        item.setdefault('comic_url', '')
        item.setdefault('comic_cover_img', '')
        item.setdefault('version', {
            "main": {
                "chapters": []
            },
            "duck": {"chapters": []},
            'rock': {"chapters": []},
            'fox': {"chapters": []},
        })
        # print(f'process_item: {item}')

        for comic in self.my_comics:
            if (comic["website_name"] == item["website_name"]):
                comic["comics"].append({
                    "name": item['comic_name'],
                    "url": item['comic_url'],
                    "cover_img": item['comic_cover_img'],
                    "version": item['version'],
                })
                print("i found it!")
                break
            else:
                print("Found nothing!")
                comic = None

                self.my_comics.append({
                    "website_name": item["website_name"],
                    "website_url": item["website_url"],
                    "comics": [{
                        "name": item['comic_name'],
                        "url": item['comic_url'],
                        "cover_img": item['comic_cover_img'],
                        "version": item['version']
                    }]
                })
        # self.my_comics.append(dict(item))
        return self.my_comics
