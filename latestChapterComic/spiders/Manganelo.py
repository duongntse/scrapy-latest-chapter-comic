
""" ___Using with $scrapy crawl spider_name ___
"""
from helpermoment import HelperMoment  # Using for running command $python3 run.py
from items import ComicItem  # Using for running command $python3 run.py
import re
import moment
import scrapy
# from latestChapterComic.items import ComicItem
# from latestChapterComic.helpermoment import HelperMoment


""" ___Using with $python3 run.py___
"""


class ManganeloSpider(scrapy.Spider):
    name = 'manganelolegendofnorthernblade'

    start_urls = [
        'https://manganelo.com/manga/sw923218',
    ]

    custom_settings = {
        # 'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'LOG_FILE': 'logs/ManganeloSpider.log',
        'LOG_LEVEL': 'DEBUG'
    }

    def getComicName(self, response):
        css_h1_tag = 'body > div.body-site:nth-child(1) > div.container.container-main:nth-child(3) > div.container-main-left:nth-child(1) > div.panel-story-info:nth-child(5) > div.story-info-right:nth-child(2) > h1:nth-child(1)'
        comic_name = response.css(css_h1_tag).css('::text').get().strip(' ,\n')
        return comic_name

    def getCoverImage(self, response):
        css_cover_img_tag = 'body > div.body-site:nth-child(1) > div.container.container-main:nth-child(3) > div.container-main-left:nth-child(1) > div.panel-story-info:nth-child(5) > div.story-info-left:nth-child(1) > span.info-image:nth-child(1) > img.img-loading:nth-child(1)'
        cover_img = response.css(css_cover_img_tag).css(
            '::attr(src)').get().strip(' ,\n')
        return cover_img

    def getChapters(self, response):
        css_ul_tag = 'body > div.body-site:nth-child(1) > div.container.container-main:nth-child(3) > div.container-main-left:nth-child(1) > div.panel-story-chapter-list:nth-child(7) > ul.row-content-chapter:nth-child(2)'
        chapterSelectors = response.css(
            css_ul_tag).css('li.a-h:nth-child(-n+10)')
        chapters = []
        for cs in chapterSelectors[0:20]:
            chapter_url = cs.css('a.chapter-name::attr(href)').get()
            chapter_text = cs.css(
                'a.chapter-name').css('::text').get().strip(' ,\n')
            time = cs.css(
                'span.chapter-time').css('::attr(title)').get()
            time = moment.date(time).format("DD MMMM YYYY HH:mm:ss")
            chapters.append({
                "link": chapter_url,
                "text": chapter_text,
                "title": "",
                "time": time
            })
        return chapters

    def parse(self, response):
        # css
        website_name = 'Manganelo'
        website_url = 'https://manganelo.com'

        # css('::attr(style)').re_first(r'url\(([^\)]+)') will return "https://abc-xyz-name.png"
        comic_name = self.getComicName(response)
        cover_img = self.getCoverImage(response)
        comic_url = response.url

        chapters = self.getChapters(response)

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
