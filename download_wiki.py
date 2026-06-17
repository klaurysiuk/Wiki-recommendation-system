from scrapy.crawler import CrawlerProcess
from Crawler import WikiSpider
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(WikiSpider)
    process.start()