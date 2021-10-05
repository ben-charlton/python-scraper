# python-scraper
Simple web scraper built using the Python library 'Scrapy'

## Running the crawler
Firstly, clone this repository into your own directory of choice
```bash
$ git clone https://github.com/ben-charlton/python-scraper.git
```

Then, run the spider with the following command
```bash
$ scrapy crawl redditbot 
```

With the current settings in _settings.py_, this will export the data as a CSV feed.
