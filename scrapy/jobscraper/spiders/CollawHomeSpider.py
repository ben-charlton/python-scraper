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
import re
import math


class CollawHomeSpider(scrapy.Spider):

    # This is the name of the bot that we use in the scrape command
    name = "collaw"
    allowed_domains = ["collaw.com"]
    start_urls = ["https://jobs.collaw.com/jobs/", ]
    
    # This begins the crawling
    def start_requests(self): 
        for url in self.start_urls: 
            yield SplashRequest(url, self.parse, 
                endpoint='render.html', 
                args={'wait': 0.5}, 
           ) 

    def parse(self, response):

        # Because of the way the college of law jobs home page is structured,
        # it shows 20 results 'per page' (although you are just clicking 'load more')
        # so we can grab the search id from the page to act as though we've clicked load more

        # First, find the total number of jobs found 
        job_count = response.css("h1.search-results__title::text").get()
        job_count = int(re.findall('\d+|$', job_count)[0]) 

        # Then we find the particular searchId from the hidden field
        search_id = response.css("form.form-inline > input[name=searchId]").extract_first()
        search_id = float(re.findall('\d+\.\d+|$', search_id)[0])

        # And hence we can find the number of 'pages' that we will need to crawl
        pages =  math.ceil(job_count / 20.0)
        for page in range(2, pages):
            url = 'https://jobs.collaw.com/jobs/?searchId={}&action=search&page={}'.format(search_id, page)
            yield Request(url, callback = self.parse_next_page)


    def parse_next_page(self, response):

        # This is the function that will grab the job information
        self.log('\n Crawling  %s\n' % response.url)
        jobs = []
        for job in response.css('.listing-item__jobs'):
            item = {}
            item['job_title'] = str(job.css("div.listing-item__title > a::text").get())
            item['job_type'] = str(job.css("span.listing-item__employment-type::text").get())
            item['date_posted'] = str(job.css("div.listing-item__date::text").get()).strip()
            item['company'] = str(job.css("span.listing-item__info--item-company::text").get()).strip()
            item['description'] = str(job.css("div.listing-item__desc::text").get()).strip()
            jobs.append(item)

        # and append these jobs to the file
        with open(f'home_jobs.json', 'a', encoding='utf8', newline='') as output_file:
            json.dump(jobs, output_file, indent=4)

        return


