import scrapy
from scrapy_splash import SplashRequest
import json

class CollawbotSpider(scrapy.Spider):
    name = 'collawbot'
    allowed_domains = ['https://jobs.collaw.com/jobs/']
    start_urls = ['http://https://jobs.collaw.com/jobs//']
    
    def start_requests(self):
        url=input()
        yield SplashRequest(url=url, callback=self.parse)

    def parse(self, response):
        jobs = []

        with open(f'{file_name}.json', 'w', encoding='utf8', newline='') as output_file:
            json.dump(jobs, output_file)

