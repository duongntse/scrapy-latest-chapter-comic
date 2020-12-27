from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from spiders.Mangapark import MangaparkSpider
from spiders.Murimlogin import MurimloginSpider
from spiders.Manganelo import ManganeloSpider
from spiders.NetTruyen import NettruyenSpider
from spiders.Blackclover import BlackcloverSpider
import os
from pathlib import Path
import shutil


def run():
    configure_logging()
    # importing project settings for further usage
    # mainly because of the middlewares
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    # running spiders sequentially (non-distributed)
    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(MangaparkSpider)
        yield runner.crawl(MurimloginSpider)
        yield runner.crawl(ManganeloSpider)
        yield runner.crawl(NettruyenSpider)
        yield runner.crawl(BlackcloverSpider)
        reactor.stop()

    crawl()
    reactor.run()  # block until the last call


run()
