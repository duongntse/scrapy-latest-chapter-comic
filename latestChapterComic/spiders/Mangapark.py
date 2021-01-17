
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


class MangaparkSpider(scrapy.Spider):
    name = 'mangapark'

    start_urls = [
        'https://mangapark.net/manga/one-piece',
        'https://mangapark.net/manga/red-storm',
        'https://mangapark.net/manga/the-undefeatable-swordsman',
        'https://mangapark.net/manga/boruto-naruto-next-generations',
        'https://mangapark.net/manga/re-monster',
        'https://mangapark.net/manga/fights-break-sphere',
        'https://mangapark.net/manga/gosu',
        'https://mangapark.net/manga/tales-of-demons-and-gods-mad-snail'
    ]

    custom_settings = {
        # 'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'LOG_FILE': 'logs/MangaparkSpider.log',
        'LOG_LEVEL': 'DEBUG'
    }

    def getChapters(self, response, stream):
        css_div_stream = f'div{stream}'
        css_ul_tag = f'div{stream} > div.volume > ul.chapter'
        css_first_5_li_tags = 'li.item:nth-child(-n+10)'

        chapters_selectors = response.css(
            css_div_stream).css(css_first_5_li_tags)
        chapters = []
        for chapter_selector in chapters_selectors[0:20]:
            chapter_link = chapter_selector.css('div.ext').css(
                'a:nth-child(5)::attr(href)').get()
            chapter_url = response.urljoin(chapter_link)
            chapter_text = chapter_selector.css(
                'div.tit>a.ch').css('::text').get()
            # print(chapter_text)
            chapter_time = chapter_selector.css('div.ext > span.time').css(
                '::text').get().strip(' ,\n')
            raw_time = HelperMoment().getRawTime(chapter_time)
            chapters.append({
                "link": chapter_url,    # "https://mangapark.net/manga/re-monster/i2610850/c67"
                "text": chapter_text,   # "ch.67"
                "title": "",            # ""
                "time": raw_time        # "01 December 2020 05:34:39"
            })

        return chapters

    def versionDuck(self, response):
        # print("versionDuck")
        stream = '#stream_4'
        return self.getChapters(response, stream)
        """
            "chapters": [
                {
                    "link": "https://mangapark.net/manga/re-monster/i2610850/c67",
                    "text": "ch.67",
                    "title": "",
                    "time": "01 December 2020 05:34:39"
                }
            ]
         """

    def versionRock(self, response):
        # print("versionRock")
        stream = '#stream_6'
        return self.getChapters(response, stream)

    def versionFox(self, response):
        # print("versionFox")
        stream = '#stream_1'
        return self.getChapters(response, stream)

    def versionPanda(self, response):
        # print("versionPanda")
        stream = '#stream_3'
        return self.getChapters(response, stream)

    def parse(self, response):
        website_name = 'Mangapark'
        website_url = 'https://mangapark.net'
        comic_url = response.url
        # comic_name_regex = rf'{website_url}/manga/(.*)'
        # comic_name = re.search(comic_name_regex, comic_url).groups()[0]

        css_title_h2_tag = 'section.manga div.container.content div.hd h2 a'
        comic_name = response.css(css_title_h2_tag).css('::text').get()

        css_cover_img_tag = 'body > section.manga:nth-child(2) > div.container.content > div.row:nth-child(2) > div.col-12.col-md-3:nth-child(1) > div.cover > img'
        cover_img = response.css(
            css_cover_img_tag).css('::attr(src)').get()

        duck = self.versionDuck(response)
        rock = self.versionRock(response)
        fox = self.versionFox(response)
        panda = self.versionPanda(response)

        # Populate the item
        item = ComicItem()
        item['website_name'] = website_name
        item['website_url'] = website_url
        item['comic_name'] = comic_name
        item['comic_url'] = comic_url
        item['cover_img'] = cover_img
        item['main_chapters'] = []
        item['duck_chapters'] = duck
        item['rock_chapters'] = rock
        item['fox_chapters'] = fox
        item['panda_chapters'] = panda

        yield {
            'website_name': website_name,
            'website_url': website_url,
            "comic_name": comic_name,
            "comic_url": comic_url,
            "cover_img": cover_img,
            "main_chapters": [],
            "duck_chapters": duck,
            'rock_chapters': rock,
            'fox_chapters': fox,
            'panda_chapters': panda,
        }
