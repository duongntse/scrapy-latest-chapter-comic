# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class LatestchaptercomicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ComicItem(Item):
    base_site_name = Field()
    base_site_url = Field()
    comic_name = Field()
    cover_img = Field()
    chapter_number_link = Field()
    chapter_number_text = Field()
    chapter_title = Field()
    raw_time = Field()
    comic_url = Field()
    prev_chap = Field()
