
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
        'http://www.nettruyen.com/truyen-tranh/hoi-sinh-the-gioi-15852'
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
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
        print(f"raw_time: {raw_time}")
        return raw_time.format("DD MMMM YYYY hh:mm:ss")

    def parse(self, response):
        comic_url = response.url
        base_site_name = 'Nettruyen'
        base_site_url = 'http://www.nettruyen.com'

        css_cover_img = 'article#item-detail div.col-image img'

        cover_img = response.css(css_cover_img).css('::attr(src)').get()
        comic_name = response.css('h1.title-detail').css('::text').get()

        # print(f'cover_img: {cover_img}')
        # print(f'comic_name: {comic_name}')

        new_chapter = response.css('div.list-chapter').css('li.row:nth-child(2)')

        chapter_number_text = new_chapter.css('div.chapter').css('a::text').get()

        chapter_number_link = new_chapter.css('div.chapter').css('a::attr(href)').get()

        chapter_title = ""

        time = new_chapter.css('div:nth-child(2)').css('::text').get().strip(' ,\n')

        raw_time = ''
        timeFrom = ''
        isTimeFrom = re.search(r'(\d+) (năm|tháng|tuần|ngày|giờ|phút|giây) (trước)', time) is not None
        isTimeRaw = re.search(r'\w{1,3}-\d{1,2}-\d{4}\s\d{2}:\d{1,2}', time) is not None
        isTimeRaw2 = re.search(r'\d{1,2}:\d{1,2}\s\d{1,2}\/\d{1,2}', time) is not None
        # print(f'isTimeFrom: {isTimeFrom}')
        print(f'TimeRaw: {time}')

        if (isTimeFrom):
            # print(f'time: {time}')
            timeFrom = HelperMoment().timeFromVnToEn(time)
            # print(f'timeFrom: {timeFrom}')
            # yield timeFrom
            raw_time = HelperMoment().getRawTime(timeFrom)
        if (isTimeRaw):
            raw_time = moment.date(time).format("DD MMMM YYYY hh:mm:ss")
        if (isTimeRaw2):  # '23:52 06/10'
            raw_time = self.makeRawtime2(time)

            # raw_time = moment.date(time).format("DD MMMM YYYY hh:mm:ss")

        # print(f'timeFrom: {timeFrom}')
        # print(f'raw_time: {raw_time}')

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
