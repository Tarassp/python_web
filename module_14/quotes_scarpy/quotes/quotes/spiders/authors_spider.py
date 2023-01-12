import scrapy
from quotes.items import AuthorItem


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    start_urls = [
        'https://quotes.toscrape.com/page/1/',
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'quotes.pipelines.AuthorsPipeline': 300,
        }
    }

    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_authors)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_authors(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        item = AuthorItem()
        item['name'] = extract_with_css('.author-title::text')
        item['birthdate'] = extract_with_css('.author-born-date::text')
        item['bio'] = extract_with_css('.author-description::text')
        yield item



