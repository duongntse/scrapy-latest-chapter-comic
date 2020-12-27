import re
import moment
import scrapy
import json
from items import ComicItem  # Using for running command $python3 run.py
from helpermoment import HelperMoment


class BlackcloverSpider(scrapy.Spider):
    name = 'blackclover'
    page = 1
    comic_url = "https://readblackclover.online"
    base_site_name = 'Readblackclover'
    base_site_url = 'https://readblackclover.online'
    cover_img = None
    comic_name = None
    chapter_number_text = None
    chapter_number_link = None
    chapter_title = None
    prev_chap = {
        "chapter_number_text": None,
        "chapter_number_link": None
    }
    raw_time = moment.now().format('DD MMM YYYY hh:mm:ss')

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
        raw_time = moment.date(data['date']).format('DD MMM YYYY HH:mm:ss')
        return raw_time

    def getCoverImg(self, response, css_cover_img):
        if(self.cover_img is None):
            self.cover_img = response.css(
                css_cover_img).css('::attr(src)').get()

    def getComicName(self, response, css_header_title):
        if(self.comic_name is None):
            self.comic_name = response.css(
                css_header_title).css('::text').get()

    def getNewChapterLinkText(self, response, css_chapter_li, css_prevchapter_li):
        new_chapter = response.css(css_chapter_li)

        if(self.chapter_number_text is None):
            self.chapter_number_text = new_chapter.css(
                'a::text').get().split(',')[1].strip(' ')

        if(self.chapter_number_link is None):
            self.chapter_number_link = new_chapter.css('a::attr(href)').get()

    def getPrevChapterLinkText(self, response, css_chapter_li, css_prevchapter_li):
        new_chapter = response.css(css_chapter_li)

        if(self.prev_chap["chapter_number_text"] is None):
            self.prev_chap["chapter_number_text"] = response.css(
                css_prevchapter_li).css('a::text').get().split(',')[1].strip(' ')

        if(self.prev_chap["chapter_number_link"] is None):
            self.prev_chap["chapter_number_link"] = response.css(
                css_prevchapter_li).css('a::attr(href)').get()

    def getNewChapterTime(self, response):
        data_conf = response.css(
            'div.wpcdt-date-conf').css('::attr(data-conf)').get()

        if(data_conf is not None):
            self.page = 2
            self.raw_time = self.getTimeCount(response)

    def parse(self, response):
        print("parse")
        css_cover_img = 'li.blocks-gallery-item figure img.wp-image-1947'
        css_header_title = 'header.entry-header > h1.entry-title'
        css_chapter_li = 'li#ceo_latest_comics_widget-3 > ul > li:nth-child(1)'
        css_prevchapter_li = 'li#ceo_latest_comics_widget-3 > ul > li:nth-child(2)'
        # ----------------------------------------------
        self.getCoverImg(response, css_cover_img)

        # ----------------------------------------------
        self.getComicName(response, css_header_title)

        # ----------------------------------------------
        self.getNewChapterLinkText(
            response, css_chapter_li, css_prevchapter_li)

        self.getPrevChapterLinkText(
            response, css_chapter_li, css_prevchapter_li)

        # ----------------------------------------------
        self.getNewChapterTime(response)

        # ----------------------------------------------
        if (self.chapter_number_link is not None):
            yield response.follow(self.chapter_number_link, self.parse)

        if(self.page == 2):
            # Populate the item
            item = ComicItem()
            item['base_site_name'] = self.base_site_name
            item['base_site_url'] = self.base_site_url
            item['cover_img'] = self.cover_img
            item['comic_name'] = self.comic_name
            item['chapter_number_link'] = response.urljoin(
                self.chapter_number_link)
            item['chapter_number_text'] = self.chapter_number_text
            item['chapter_title'] = self.chapter_title
            item['raw_time'] = self.raw_time
            item['comic_url'] = self.comic_url
            item['prev_chap'] = self.prev_chap

            yield {
                'base_site_name': self.base_site_name,
                'base_site_url': self.base_site_url,
                'chapter_number_link': response.urljoin(self.chapter_number_link),
                'chapter_number_text': self.chapter_number_text,
                'chapter_title': self.chapter_title,
                'comic_name': self.comic_name,
                'cover_img': self.cover_img,
                'raw_time': self.raw_time,
                'comic_url': self.comic_url,
                'prev_chap': self.prev_chap
            }
