
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

    def parse(self, response):
        comic_url = response.url
        base_site_name = 'Mangakakalot'
        base_site_url = 'https://mangakakalot.com'

        css_img_tag = 'body > div.container:nth-child(2) > div.main-wrapper:nth-child(2) > div.leftCol:nth-child(1) > div.manga-info-top:nth-child(3) > div.manga-info-pic:nth-child(1) > img:nth-child(1)'
        css_title_h1 = 'div.manga-info-top ul.manga-info-text li h1'

        cover_img = response.css(css_img_tag).css('::attr(src)').get()
        comic_name = response.css(css_title_h1).css('::text').get()
        new_chapter = response.css(
            'div.chapter-list').css('div.row:nth-child(1)')
        chapter_number_text = new_chapter.css(
            'span:nth-child(1)').css('a::text').get()
        chapter_number_link = new_chapter.css(
            'span:nth-child(1)').css('a::attr(href)').get()
        chapter_title = new_chapter.css(
            'span:nth-child(1)').css('a::attr(title)').get()
        time = new_chapter.css(
            'span:nth-child(3)::attr(title)').get().strip(' ,\n')

        # if (re.search(r'\w{1,3}-\d{1,2}-\d{4}\s\d{2}:\d{1,2}', time) is not None):
        #     time = HelperMoment().fromNow(time)

        raw_time = moment.date(time).format("DD MMMM YYYY hh:mm:ss")

        print(f'time: {time}')
        print(f'raw_time: {raw_time}')

        # Populate the item
        item = ComicItem()
        item['base_site_name'] = base_site_name
        item['base_site_url'] = base_site_url
        item['cover_img'] = cover_img
        item['comic_name'] = comic_name
        item['chapter_number_link'] = response.urljoin(chapter_number_link)
        item['chapter_number_text'] = chapter_number_text
        item['chapter_title'] = chapter_title
        item['raw_time'] = raw_time
        item['comic_url'] = comic_url

        yield {
            'base_site_name': base_site_name,
            'base_site_url': base_site_url,
            'chapter_number_link': response.urljoin(chapter_number_link),
            'chapter_number_text': chapter_number_text,
            'chapter_title': "",
            'comic_name': comic_name,
            'cover_img': cover_img,
            'raw_time': raw_time,
            'comic_url': comic_url,
        }
