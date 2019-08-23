from multiprocessing import Process, Queue
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings

SPIDER_NAMES = ['cs_scut', 'jnu', 'lois', 'pku',
                'scau', 'se_scut', 'sjtu', 'th']


def crawl_all(spider_names=SPIDER_NAMES):
    process = CrawlerProcess(get_project_settings())
    for spider in spider_names:
        process.crawl(spider)
    process.start()


if __name__ == "__main__":
    crawl_all(SPIDER_NAMES)
