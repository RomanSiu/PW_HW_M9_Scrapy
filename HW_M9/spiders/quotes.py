import scrapy
from HW_M9.items import AuthorsScrapyItem, QuotesScrapyItem


urls_to_scrape = []


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse_quotes(self, raw_quote):
        quote = QuotesScrapyItem()

        quote["quote"] = raw_quote.xpath("span[@class='text']/text()").get()
        quote["author"] = raw_quote.xpath("span/small[@class='author']/text()").get()
        quote["tags"] = raw_quote.xpath("div/a[@class='tag']/text()").getall()

        return quote

    def parse(self, response):
        quotes = response.xpath("/html//div[@class='quote']")
        for quote in quotes:
            yield self.parse_quotes(quote)

            author_link = f"{self.start_urls[0]}{quote.xpath('span/a/@href').get()}"
            if author_link not in urls_to_scrape:
                urls_to_scrape.append(scrapy.Request(author_link))

            next_page = response.xpath("//li[@class='next']/a/@href").get()

            if next_page is not None:
                yield scrapy.Request(url=self.start_urls[0] + next_page)


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]

    def start_requests(self):
        for url in urls_to_scrape:
            yield url

    def parse(self, response):
        author = AuthorsScrapyItem()

        author["fullname"] = response.xpath("//div/h3[@class='author-title']/text()").get()
        author["born_date"] = response.xpath("//div/p/span[@class='author-born-date']/text()").get()
        author["born_location"] = response.xpath("//div/p/span[@class='author-born-location']/text()").get()
        author["description"] = response.xpath("//div[@class='author-description']/text()").get()

        yield author