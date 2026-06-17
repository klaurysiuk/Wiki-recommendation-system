from scrapy.crawler import CrawlerProcess
from Crawler import WikiSpiderOne
import sys
if __name__ == "__main__":
    urls = sys.argv[1]
    urls = urls.split(',')
    process = CrawlerProcess()
    process.crawl(WikiSpiderOne, urls = urls)
    process.start()