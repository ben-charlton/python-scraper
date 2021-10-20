# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
import json
    

class IndeedItem(Item):
    # define the fields for your item here like:
    job_title = Field()
    link_url = Field()
    location = Field()
    company = Field()
    summary = Field()
    source = Field()
    found_date = Field()
    source_url = Field()
    source_page_body = Field()
    crawl_url = Field()
    crawl_timestamp = Field()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    pass