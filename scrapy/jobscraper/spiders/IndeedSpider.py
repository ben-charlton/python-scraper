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


class IndeedSpider(scrapy.Spider):
    name = "indeed"
    allowed_domains = ["indeed.com"]
    start_urls = ["https://au.indeed.com/jobs?q=&l=Sydney+NSW", ]
    
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
        hxs = Selector(response)
        sites = hxs.select("//div[@class='row ' or @class='row lastRow']")
        jobs = []
        for site in sites:
            item = IndeedItem(company='none')

            item['job_title'] = site.select('h2/a/@title').extract()
            link_url = site.select('h2/a/@href').extract()
            item['link_url'] = link_url
            item['crawl_url'] = response.url
            item['location'] = site.select("span[@class='location']/text()").extract()

            # Not all entries have a company
            if site.select("span[@class='company']/text()").extract() == []:
                item['company'] = [u'']
            else:
                item['company'] = site.select("span[@class='company']/text()").extract()
                item['summary'] = site.select("//table/tr/td/span[@class='summary']").extract()
                item['source'] = site.select("table/tr/td/span[@class='source']/text()").extract()
                item['found_date'] = site.select("table/tr/td/span[@class='date']/text()").extract()
                request = Request("http://www.indeed.com" + item['link_url'][0], callback=self.parse_next_site)
                request.meta['item'] = item
                yield request
                jobs.append(item)

        with open(f'jobs.json', 'w', encoding='utf8', newline='') as output_file:
            json.dump(jobs, output_file)

        return


SPIDER = IndeedSpider()
