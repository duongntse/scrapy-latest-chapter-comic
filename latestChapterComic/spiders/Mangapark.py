
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
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
    }

    def versionDuck(self):
        stream = '#stream_4'
#
    def versionRock(self):
        stream = '#stream_6'
#
    def versionFox(self):
        stream = '#stream_1'
#

    def parse(self, response):
        base_site_name = 'Mangapark'
        base_site_url = 'https://mangapark.net'
        manga_name_regex = rf'{base_site_url}/manga/(.*)'
        comic_url = response.url
        stream = '#stream_4'
        onepiece = '#stream_3'
        borutoNextGen = '#stream_3'
        redstorm = '#stream_3'
        undefeatableSwordsman = '#stream_4'
        reMonster = '#stream_4'
        dauphathuongkhung = '#stream_4'
        talesofdemonsandgodsmadsnail = '#stream_4'
        gosu = '#stream_1'

        manga_name = re.search(manga_name_regex, comic_url).groups()[0]

        print(f'manga_name: {manga_name}')

        if(manga_name == 'one-piece'):
            stream = onepiece
        if(manga_name == 'red-storm'):
            stream = redstorm
        if(manga_name == 'the-undefeatable-swordsman'):
            stream = undefeatableSwordsman
        if(manga_name == 'boruto-naruto-next-generations'):
            stream = borutoNextGen
        if(manga_name == 're-monster'):
            stream = reMonster
        if(manga_name == 'fights-break-sphere'):
            stream = dauphathuongkhung
        if(manga_name == 'tales-of-demons-and-gods-mad-snail'):
            stream = talesofdemonsandgodsmadsnail
        if(manga_name == 'gosu'):
            stream = gosu

        print(f'stream: {stream}')
        css_cover_img_tag = 'body > section.manga:nth-child(2) > div.container.content > div.row:nth-child(2) > div.col-12.col-md-3:nth-child(1) > div.cover > img'
        css_ul_tag = f'div{stream} > div.volume > ul.chapter'
        css_first_li_tag = 'li.item:nth-child(1)'
        css_title_h2_tag = 'body > section.manga:nth-child(2) > div.container.content > div.pb-1.mb-2.line-b-f.hd:nth-child(1) > h2'

        cover_img = response.css(css_cover_img_tag).css('::attr(src)').get()
        comic_name = response.css(css_title_h2_tag).css('a::text').get()
        latest_chapter = response.css(css_ul_tag).css(css_first_li_tag)
        chapter_number_link = latest_chapter.css('div.ext').css(
            'a:nth-child(5)::attr(href)').get()
        full_chapter_url = response.urljoin(chapter_number_link)
        chapter_number_text = latest_chapter.css(
            'div.tit>a.ch').css('::text').get()
        time = latest_chapter.css('div.ext > span.time').css(
            '::text').get().strip(' ,\n')
        raw_time = HelperMoment().getRawTime(time)

        # Populate the item
        item = ComicItem()
        item['base_site_name'] = base_site_name
        item['base_site_url'] = base_site_url
        item['chapter_number_link'] = full_chapter_url
        item['chapter_number_text'] = chapter_number_text
        item['chapter_title'] = ""
        item['comic_name'] = comic_name
        item['cover_img'] = cover_img
        item['raw_time'] = raw_time
        item['comic_url'] = comic_url

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
