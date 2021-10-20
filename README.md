# python-scraper
Simple web scraper built using the Python library 'Scrapy'

## Running the crawler
Firstly, clone this repository into your own directory of choice
```bash
$ git clone https://github.com/ben-charlton/python-scraper.git
```
### Dependencies
You will need Python2+ and the Scrapy and Splash modules
```bash
$ pip install -r requirements.txt
```

You will also need install docker, as the easiest way to set up splash is through docker.
This can be done with a number of commands dependent on OS, but for Mac OS set up with a 
package manager like HomeBrew - 
```bash
$ brew cask install docker
```

Then, run Splash on the localhost using 
```bash
$ docker run -p 8050:8050 scrapinghub/splash
```

Then, run the spider with the following commands
```bash
$ cd scrapy 
```
```bash
$ scrapy crawl <bot name> 
```

With the current settings in _settings.py_, this will export the data as a json file.
