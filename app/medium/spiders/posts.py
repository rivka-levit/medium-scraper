import scrapy


class PostsSpider(scrapy.Spider):
    name = "posts"
    allowed_domains = ["medium.com"]
    start_urls = ["https://medium.com"]

    def parse(self, response, **kwargs):
        pass
