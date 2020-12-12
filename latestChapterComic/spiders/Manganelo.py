
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
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
    }

    def parse(self, response):
        # css
        base_site_name = 'Manganelo'
        base_site_url = 'https://manganelo.com'
        css_cover_img_tag = 'body > div.body-site:nth-child(1) > div.container.container-main:nth-child(3) > div.container-main-left:nth-child(1) > div.panel-story-info:nth-child(5) > div.story-info-left:nth-child(1) > span.info-image:nth-child(1) > img.img-loading:nth-child(1)'
        css_h1_tag = 'body > div.body-site:nth-child(1) > div.container.container-main:nth-child(3) > div.container-main-left:nth-child(1) > div.panel-story-info:nth-child(5) > div.story-info-right:nth-child(2) > h1:nth-child(1)'
        css_ul_tag = 'body > div.body-site:nth-child(1) > div.container.container-main:nth-child(3) > div.container-main-left:nth-child(1) > div.panel-story-chapter-list:nth-child(7) > ul.row-content-chapter:nth-child(2)'

        cover_img = response.css(css_cover_img_tag).css(
            '::attr(src)').get().strip(' ,\n')
        # css('::attr(style)').re_first(r'url\(([^\)]+)') will return "https://abc-xyz-name.png"

        comic_name = response.css(css_h1_tag).css('::text').get().strip(' ,\n')
        new_chapter = response.css(css_ul_tag).css('li.a-h:nth-child(1)')
        full_chapter_url = new_chapter.css('a.chapter-name::attr(href)').get()
        chapter_number_text = new_chapter.css(
            'a.chapter-name').css('::text').get().strip(' ,\n')
        # timeFrom = new_chapter.css(
        #     'span.chapter-time').css('::text').get().strip(' ,\n')
        time = new_chapter.css(
            'span.chapter-time').css('::attr(title)').get()
        # raw_time = HelperMoment().getRawTime(timeFrom)
        raw_time = moment.date(time).format("DD MMMM YYYY hh:mm:ss")
        comic_url = response.url

        # Populate the item
        item = ComicItem()

        item['base_site_name'] = base_site_name
        item['base_site_url'] = base_site_url
        item['comic_name'] = comic_name
        item['chapter_number_link'] = full_chapter_url
        item['chapter_number_text'] = chapter_number_text
        item['raw_time'] = raw_time
        item['comic_url'] = comic_url
        item['cover_img'] = cover_img
        item['chapter_title'] = ""

        yield {
            'base_site_name': base_site_name,
            'base_site_url': base_site_url,
            'chapter_number_link': full_chapter_url,
            'chapter_number_text': chapter_number_text,
            'chapter_title': "",
            'comic_name': comic_name,
            'cover_img': cover_img,
            'raw_time': raw_time,
            'comic_url': comic_url,
        }
