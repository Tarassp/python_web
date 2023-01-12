# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
from .models import db_connect, create_tables, Quote, Tag, Author
from sqlalchemy.orm import Session


class AuthorsPipeline:
    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        author = Author()
        author.name = item['name']
        author.birthdate = datetime.strptime(item['birthdate'], "%B %d, %Y").date()
        author.bio = item['bio']

        try:
            self.session.add(author)
            self.session.commit()
        except Exception as err:
            print(f"Error: {err}")

        return item


class QuotesPipeline:

    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        quote = Quote()
        quote.text = item['text']
        quote.author_name = item['author']
        for tag_item in item['tags']:
            tag = Tag(name=tag_item)
            quote.tags.append(tag)
        try:
            self.session.add(quote)
            self.session.commit()
        except Exception as err:
            print(f"Error: {err}")

        return item