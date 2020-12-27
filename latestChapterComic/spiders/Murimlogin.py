
""" ___Using for running command $scrapy crawl spider_name ___
"""
import re
import moment
import scrapy
# Using for running command $python3 run.py
from items import ComicItem  # Using for running command $python3 run.py
from helpermoment import HelperMoment
# from latestChapterComic.items import ComicItem
# from latestChapterComic.helpermoment import HelperMoment
# from latestChapterComic.spiders.helpers.helpermoment import HelperMoment


""" ___Using for running command $python3 run.py___

"""


class MurimloginSpider(scrapy.Spider):
    name = 'murimlogin'

    start_urls = [
        'https://mangakakalot.com/manga/gz922893',
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
    }

    def getComicName(self, response):
        css_title_h1 = 'div.manga-info-top ul.manga-info-text li h1'
        comic_name = response.css(css_title_h1).css('::text').get()
        return comic_name

    def getCoverImage(self, response):
        css_img_tag = 'body > div.container:nth-child(2) > div.main-wrapper:nth-child(2) > div.leftCol:nth-child(1) > div.manga-info-top:nth-child(3) > div.manga-info-pic:nth-child(1) > img:nth-child(1)'
        cover_img = response.css(css_img_tag).css('::attr(src)').get()
        return cover_img

    def getChapters(self, response):

        chapterSelectors = response.css(
            'div.chapter-list').css('div.row:nth-child(-n+5)')
        chapters = []
        for cs in chapterSelectors[0:5]:
            chapter_text = cs.css(
                'span:nth-child(1)').css('a::text').get()
            chapter_url = cs.css(
                'span:nth-child(1)').css('a::attr(href)').get()
            chapter_title = cs.css(
                'span:nth-child(1)').css('a::attr(title)').get()
            raw_time = cs.css(
                'span:nth-child(3)::attr(title)').get().strip(' ,\n')
            time = moment.date(raw_time).format("DD MMMM YYYY HH:mm:ss")
            chapters.append({
                "link": chapter_url,
                "text": chapter_text,
                "title": chapter_title,
                "time": time
            })
        return chapters

    def parse(self, response):
        comic_url = response.url
        website_name = 'Mangakakalot'
        website_url = 'https://mangakakalot.com'
        comic_name = self.getComicName(response)
        cover_img = self.getCoverImage(response)
        chapters = self.getChapters(response)

        # if (re.search(r'\w{1,3}-\d{1,2}-\d{4}\s\d{2}:\d{1,2}', time) is not None):

        # Populate the item
        item = ComicItem()
        item['website_name'] = website_name
        item['website_url'] = website_url
        item['comic_name'] = comic_name
        item['comic_url'] = comic_url
        item['cover_img'] = cover_img
        item['main_chapters'] = chapters
        item['duck_chapters'] = []
        item['rock_chapters'] = []
        item['fox_chapters'] = []
        item['panda_chapters'] = []

        yield {
            'website_name': website_name,
            'website_url': website_url,
            "comic_name": comic_name,
            "comic_url": comic_url,
            "cover_img": cover_img,
            "main_chapters": chapters,
            "duck_chapters": [],
            "rock_chapters": [],
            "fox_chapters": [],
            "panda_chapters": [],
        }
