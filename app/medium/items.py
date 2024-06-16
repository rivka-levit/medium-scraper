"""
Item model for the posts.
"""

import scrapy

from itemloaders.processors import Join


class MediumItem(scrapy.Item):
    title = scrapy.Field(output_processor=Join())
    excerpt = scrapy.Field(output_processor=Join())
    link = scrapy.Field(output_processor=Join())
