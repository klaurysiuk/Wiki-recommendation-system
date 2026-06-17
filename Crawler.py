import scrapy
from urllib.parse import unquote
from unidecode import unidecode

class WikiSpider(scrapy.Spider):
    name = "wiki_ascii"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = [
                "https://en.wikipedia.org/wiki/Bratislava",
                "https://en.wikipedia.org/wiki/French_Revolution",
                "https://en.wikipedia.org/wiki/James_Joyce"    
                ]

    custom_settings = {
        'DEPTH_PRIORITY': 1,
        'DEPTH_LIMIT' : 1,
        'FEEDS': {'wikipedia.json': {'format': 'json', 'encoding': 'utf8', 'ensure_ascii': False}}
    }


    def parse(self, response):
        
        title = response.xpath('//h1[@id="firstHeading"]//text()').getall()
        title = ''.join(title).strip()
        paragraphs = response.xpath('//div[@id="mw-content-text"]//p//text()').getall()
        text = " ".join(p.strip() for p in paragraphs if p.strip())
    
        title_ascii = unidecode(title)
        text_ascii = unidecode(text)

        yield {
            "url": unidecode(response.url),
            "title": title_ascii,
            "text": text_ascii,
        }
        depth = response.meta.get('depth', 0)
        if depth < 1:
            for href in response.xpath('//div[@id="bodyContent"]//a[@href]/@href').getall():
                if href.startswith("/wiki/") and ":" not in href:
                    next_page = response.urljoin(href)
                    yield scrapy.Request(next_page, callback=self.parse)


class WikiSpiderOne(scrapy.Spider):
    name = "wiki_ascii"
    allowed_domains = ["en.wikipedia.org"]

    custom_settings = {
        'DEPTH_PRIORITY': 1,
        'DEPTH_LIMIT' : 1,
        'FEEDS': {'wikipedia_new.json': {'format': 'json', 'encoding': 'utf8', 'ensure_ascii': False}}
    }
    
    def __init__(self, urls=None, *args, **kwargs):
        super(WikiSpiderOne, self).__init__(*args, **kwargs)
        self.start_urls = urls
        

    def parse(self, response):
        title = response.xpath('//h1[@id="firstHeading"]//text()').getall()
        title = ''.join(title).strip()
        paragraphs = response.xpath('//div[@id="mw-content-text"]//p//text()').getall()
        text = " ".join(p.strip() for p in paragraphs if p.strip())

        title_ascii = unidecode(title)
        text_ascii = unidecode(text)

        yield {
            "url": unidecode(response.url),
            "title": title_ascii,
            "text": text_ascii,
        }
        
        depth = response.meta.get('depth', 0)
        if depth < -1:
            for href in response.xpath('//div[@id="bodyContent"]//a[@href]/@href').getall():
                if href.startswith("/wiki/") and ":" not in href:
                    next_page = response.urljoin(href)
                    yield scrapy.Request(next_page, callback=self.parse)