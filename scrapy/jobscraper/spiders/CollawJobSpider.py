import scrapy
from scrapy_splash import SplashRequest
import json
from scrapy.selector import Selector
#from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
import time
import sys
from ..items import IndeedItem
from urllib.parse import urlencode, quote_plus


class CollawJobSpider(scrapy.Spider):
    name = "collawjob"
    allowed_domains = ["collaw.com"]
    start_urls = ["https://jobs.collaw.com/job/13884/paralegal/", ]
    
    def start_requests(self): 
        for url in self.start_urls: 
            yield SplashRequest(url, self.parse, 
                endpoint='render.html', 
                args={'wait': 0.5}, 
           ) 

    def parse_next_site(self, response):

        item = response.request.meta['item']
        item['source_url'] = response.url
        item['source_page_body'] = response.body
        item['crawl_timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
        return item


    def parse(self, response):

        self.log('\n Crawling  %s\n' % response.url)
    
        item = {}
        item['job_title'] = str(response.css("h1.details-header__title::text").get())
        item['job_type'] = str(response.css("span.job-type__value::text").get())
        item['date_posted'] = str(response.css("li.listing-item__info--item-date::text").get()).strip()
        item['company'] = str(response.css("div.details-body__content:nth-child(4)::text").get()).strip()
        item['requirements'] = str(response.css("div.details-body__content > ul::text").get())
        item['email'] = str(response.css("div.pull-left details-body__left > div:nth-child(5)::text").get())

        with open(f'job.json', 'w', encoding='utf8', newline='') as output_file:
            json.dump(item, output_file, indent=4)

        return

