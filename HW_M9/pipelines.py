# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
from HW_M9.items import AuthorsScrapyItem, QuotesScrapyItem
from models import Author, Quote
import connect


class SavetoMongoDBPipeline:
    def process_item(self, item, spider):
        if isinstance(item, QuotesScrapyItem):
            self.save_quotes(item)
        elif isinstance(item, AuthorsScrapyItem):
            self.save_authors(item)

    def save_authors(self, item):
        date = datetime.strptime(item["born_date"], "%B %d, %Y")
        author = Author(fullname=item["fullname"], born_date=date, born_location=item["born_location"],
                        description=item["description"]).save()

    def save_quotes(self, item):
        quote = Quote(tags=item["tags"], author=item["author"], quote=item["quote"]).save()
