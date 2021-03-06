
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


class NettruyenSpider(scrapy.Spider):
    name = 'nettruyen'

    start_urls = [
        'http://www.nettruyen.com/truyen-tranh/tan-tac-long-ho-mon-4486',
        'http://www.nettruyen.com/truyen-tranh/dao-hai-tac-9169',
        'http://www.nettruyen.com/truyen-tranh/hiep-khach-giang-ho-4405',
        'http://www.nettruyen.com/truyen-tranh/tay-du-9884',
        'http://www.nettruyen.com/truyen-tranh/gosu-cao-thu-2-169615',
        'http://www.nettruyen.com/truyen-tranh/yeu-than-ky-105810',
        'http://www.nettruyen.com/truyen-tranh/dang-nhap-murim',
        'http://www.nettruyen.com/truyen-tranh/hoi-sinh-the-gioi-15852',
        'http://www.nettruyen.com/truyen-tranh/remonster-4049',
        'http://www.nettruyen.com/truyen-tranh/baki-son-of-ogre-9000',
        'http://www.nettruyen.com/truyen-tranh/kattobi-itto-duong-dan-den-khung-thanh-bo-1-8428',
        'http://nhattruyen.com/truyen-tranh/dau-pha-thuong-khung-4409'
    ]

    custom_settings = {
        # 'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'LOG_FILE': 'logs/NettruyenSpider.log',
        'LOG_LEVEL': 'DEBUG'
    }

    def makeRawtime2(self, time):  # '23:52 06/10'
        date_arr = time.split(' ')

        hour_minute_arr = date_arr[0].split(':')
        hour_numb = hour_minute_arr[0]
        minute_numb = hour_minute_arr[1]

        day_month_arr = date_arr[1].split('/')
        day_numb = day_month_arr[0]
        month_numb = day_month_arr[1]

        raw_time = moment.date(moment.now().year, int(month_numb), int(
            day_numb), int(hour_numb), int(minute_numb), 0)
        # print(f"raw_time: {raw_time}")
        return raw_time.format("DD MMMM YYYY HH:mm:ss")

    def makeRawtime3(self, time):  # 11/07/19
        date_arr = time.split('/')

        day_numb = date_arr[0]
        month_numb = date_arr[1]
        year_numb = date_arr[2]

        raw_time = moment.date(int(year_numb), int(month_numb), int(
            day_numb))
        # print(f"raw_time: {raw_time}")
        return raw_time.format("DD MMMM YYYY HH:mm:ss")

    def getComicName(self, response):
        comic_name = response.css('h1.title-detail').css('::text').get()
        return comic_name

    def getCoverImage(self, response):
        css_cover_img = 'article#item-detail div.col-image img'
        cover_img = response.css(css_cover_img).css('::attr(src)').get()
        return cover_img

    def getChapters(self, response):
        chapterSelectors = response.css(
            'div.list-chapter').css('li.row:nth-child(-n+11)')

        chapters = []
        for cs in chapterSelectors[1:11]:
            chapter_text = cs.css(
                'div.chapter').css('a::text').get()

            chapter_url = cs.css(
                'div.chapter').css('a::attr(href)').get()

            chapter_title = ""

            timeRaw = cs.css(
                'div:nth-child(2)').css('::text').get().strip(' ,\n')

            time = ''
            # format: 1 giờ trước / 1 ngày trước / 1 tháng trước
            isTimeFrom = re.search(
                r'(\d+) (năm|tháng|tuần|ngày|giờ|phút|giây) (trước)', timeRaw) is not None
            # format: Dec-23-2020 13:45
            isTimeRaw = re.search(
                r'\w{1,3}-\d{1,2}-\d{4}\s\d{2}:\d{1,2}', timeRaw) is not None
            # format: '23:52 06/10'
            isTimeRaw2 = re.search(
                r'\d{1,2}:\d{1,2}\s\d{1,2}\/\d{1,2}', timeRaw) is not None
            # format: 11/07/19
            isTimeRaw3 = re.search(
                r'\d{1,2}\/\d{1,2}\/\d{1,2}', timeRaw) is not None

            if (isTimeFrom):
                timeFrom = HelperMoment().timeFromVnToEn(timeRaw)
                time = HelperMoment().getRawTime(timeFrom)
            if (isTimeRaw):
                time = moment.date(timeRaw).format("DD MMMM YYYY hh:mm:ss")
            if (isTimeRaw2):  # '23:52 06/10'
                time = self.makeRawtime2(timeRaw)
            # format: 11/07/19
            if (isTimeRaw3):
                time = self.makeRawtime3(timeRaw)

            chapters.append({
                "link": chapter_url,
                "text": chapter_text,
                "title": chapter_title,
                "time": time
            })

        return chapters

    def parse(self, response):
        comic_url = response.url
        website_name = 'Nettruyen'
        website_url = 'http://www.nettruyen.com'

        cover_img = self.getCoverImage(response)
        comic_name = self.getComicName(response)

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
