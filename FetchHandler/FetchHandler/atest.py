import sys
from os.path import dirname
from scrapy.utils.project import get_project_settings

sys.path.append((dirname(dirname(__file__))))
print((dirname(dirname(__file__))))
from crawlall import crawl_all
print(get_project_settings())
crawl_all()
