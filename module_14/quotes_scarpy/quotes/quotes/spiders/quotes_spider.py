import scrapy
from quotes.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    start_urls = [
        'https://quotes.toscrape.com/page/1/',
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'quotes.pipelines.QuotesPipeline': 300,
        }
    }

    def parse(self, response):
        for quote in response.css('div.quote'):
            item = QuoteItem()
            item['text'] = quote.css('span.text::text').get()[1:-1]
            item['author'] = quote.css('small.author::text').get()
            item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield item
        yield from response.follow_all(css='ul.pager a', callback=self.parse)
