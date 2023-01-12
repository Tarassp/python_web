import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from quotes.spiders.authors_spider import AuthorsSpider
from quotes.spiders.quotes_spider import QuotesSpider


def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(AuthorsSpider)
    process.join()
    process.crawl(QuotesSpider)
    process.start()


if __name__ == '__main__':
    main()

