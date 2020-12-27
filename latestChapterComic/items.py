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
    website_name = Field()
    website_url = Field()
    comic_name = Field()
    comic_url = Field()
    cover_img = Field()
    main_chapters = Field()
    duck_chapters = Field()
    rock_chapters = Field()
    fox_chapters = Field()
    panda_chapters = Field()
