import scrapy
from os.path import dirname
import sys
import re
from ..items import InfoItem

sys.path.append(dirname(dirname(dirname(dirname(__file__)))))
from DatabaseHandler.utils import get_lecturer_nlp

URL = []


class SE_SCUT(scrapy.Spider):
    name = 'se_scut'
    start_urls = []
    n_pages = 3
    for i in range(n_pages):
        start_urls.append("http://www2.scut.edu.cn/sse/xshd/list" + str(i + 1) + ".htm")

    def parse(self, response):
        for href in response.xpath("//ul[contains(@class,'news_ul')]/li[contains(@class,'news_li')]//a//@href"):
            url = "http://www2.scut.edu.cn" + href.extract()
            # print("url: "+url)
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = InfoItem()
        title = response.xpath(
            "//div[@class='arti_cont']//h2/text()"
        ).extract()[0].strip()
        if "报告会" not in title:
            return
        description = response.xpath(
            "//meta[@name='description']/@content"
        ).extract()[0].strip()
        description = "\n".join([title, description])
        if response.request.url not in URL:
            URL.append(response.request.url)
            item['title'] = title
            item['lecturer'] = []
            lecturer = get_lecturer_nlp(title)
            if lecturer:
                item['lecturer'].append(lecturer)
            lec_time = re.findall("报告时间：(.*?)报告", description)
            if len(lec_time) != 0:
                item['lecture_time'] = lec_time[0]
            item['issued_time'] = response.xpath(
                "//span[@class='arti_update']/text()"
            ).extract()[0].split("：")[1]
            loc = re.findall("地点：(.*?厅)", description)
            if len(loc) != 0:
                item['location'] = loc[0]
            elif len(re.findall("地点：(.*?室)", description)) != 0:
                item['location'] = re.findall("地点：(.*?)室", description)[0]
            elif len(re.findall("地点：(.*?)报告时间", description)) != 0:
                item['location'] = re.findall("地点：(.*?)报告时间", description)[0]
            elif len(re.findall("地点：(.*?)欢迎", description)) != 0:
                item['location'] = re.findall("地点：(.*?)欢迎", description)[0]
            item['url'] = response.request.url
            item['uni'] = 'SCUT'
            item['description'] = description
            yield item
        return
