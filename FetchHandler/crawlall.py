from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

spider_names = ['cs_scut', 'jnu', 'lois', 'pku',
                'scau', 'se_scut', 'sjtu', 'th']

for spider in spider_names:
    process.crawl(spider)

if __name__ == "__main__":
    process.start()
