import re
import moment
import scrapy
import json
from items import ComicItem  # Using for running command $python3 run.py
from helpermoment import HelperMoment
import itertools as iter


class BlackcloverSpider(scrapy.Spider):
    name = 'blackclover'
    page = 1
    comic_url = "https://readblackclover.online"
    website_name = 'Readblackclover'
    website_url = 'https://readblackclover.online'
    cover_img = None
    comic_name = None
    newChapter = None
    oldChapters = []

    start_urls = [
        'https://readblackclover.online/',
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
    }

    def getTimeCount(self, response):
        data_conf = response.css(
            'div.wpcdt-date-conf').css('::attr(data-conf)').get()
        data = json.loads(data_conf)
        # raw_time = moment.date(data['date']).format('DD MMM YYYY hh:mm:ss A')
        raw_time = moment.date(data['date']).format('DD MMM YYYY HH:mm:ss ')
        print("Blackclover, getTimeCount(self,response), raw_time: ")
        print(raw_time)
        return raw_time

    def getCoverImg(self, response, css_cover_img):
        if(self.cover_img is None):
            self.cover_img = response.css(
                css_cover_img).css('::attr(src)').get()

    def getComicName(self, response, css_header_title):
        if(self.comic_name is None):
            self.comic_name = response.css(
                css_header_title).css('::text').get()

    def getNewChapterTime(self, response):
        data_conf = response.css(
            'div.wpcdt-date-conf').css('::attr(data-conf)').get()

        if(data_conf is not None):
            self.page = 2
            self.newChapter["time"] = self.getTimeCount(response)

    def getNewChapter(self, response):
        if(self.newChapter is None):
            css_new_chapters_li = 'li#ceo_latest_comics_widget-3 > ul > li:nth-child(1)'
            new_chapter = response.css(css_new_chapters_li)
            link = new_chapter.css('a::attr(href)').get()
            text = new_chapter.css('a::text').get().split(',')[1].strip(' ')
            self.newChapter = {"link": link,
                               "text": text,
                               "title": "",
                               "time": None}

    def getOldChapters(self, response):
        if(len(self.oldChapters) == 0):
            css_old_chapters_li = 'li#ceo_latest_comics_widget-3 > ul > li:nth-child(n+1)'
            for chapter_selector in response.css(css_old_chapters_li)[1: 20]:
                text = chapter_selector.css('a::text').get().split(',')[
                    1].strip(' ')
                link = chapter_selector.css('a::attr(href)').get()
                self.oldChapters.append({
                    "link": link,
                    "text": text,
                    "title": "",
                    "time": "",
                })

    def parse(self, response):
        css_cover_img = 'li.blocks-gallery-item figure img.wp-image-1947'
        css_header_title = 'header.entry-header > h1.entry-title'

        self.getCoverImg(response, css_cover_img)
        self.getComicName(response, css_header_title)
        self.getNewChapter(response)
        self.getNewChapterTime(response)
        self.getOldChapters(response)

        if(self.newChapter is not None):
            if(self.newChapter["link"] is not None):
                yield response.follow(self.newChapter["link"], self.parse)

        # Populate the item
        if(self.page == 2):
            chapters = []
            chapters.append(self.newChapter)
            chapters.extend(self.oldChapters)
            item = ComicItem()
            item['website_name'] = self.website_name
            item['website_url'] = self.website_url
            item['comic_name'] = self.comic_name
            item['comic_url'] = self.comic_url
            item['cover_img'] = self.cover_img
            item['main_chapters'] = chapters
            item['duck_chapters'] = []
            item['rock_chapters'] = []
            item['fox_chapters'] = []
            item['panda_chapters'] = []

            yield {
                'website_name': self.website_name,
                'website_url': self.website_url,
                "comic_name": self.comic_name,
                "comic_url": self.comic_url,
                "cover_img": self.cover_img,
                "main_chapters": chapters,
                "duck_chapters": [],
                "rock_chapters": [],
                "fox_chapters": [],
                "panda_chapters": [],
            }
