import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from HW_M9.spiders.quotes import AuthorsSpider, QuotesSpider


def main():
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(QuotesSpider)
        yield runner.crawl(AuthorsSpider)
        reactor.stop()

    crawl()
    reactor.run()


if __name__ == '__main__':
    main()
