import scrapy
from os.path import dirname
import sys
from ..items import InfoItem

sys.path.append(dirname(dirname(dirname(dirname(__file__)))))
from DatabaseHandler.utils import get_lecturer_nlp

URL = []


class CS_SCUT(scrapy.Spider):
    name = 'cs_scut'
    start_urls = []
    n_pages = 3
    for i in range(n_pages):
        start_urls.append(
            "http://www2.scut.edu.cn/cs/22333/list" + str(i + 1) + ".htm"
        )

    def parse(self, response):
        for href in response.xpath("//h2[@class='notice-title']/a/@href"):
            if "redirect" not in href.extract():
                url = "http://www2.scut.edu.cn" + href.extract()
                yield scrapy.Request(url, callback=self.parse_dir_contents)
            # not in school of cs
            else:
                return

    def parse_dir_contents(self, response):
        item = InfoItem()
        title = response.xpath(
            "//h2[@class='info-title']/text()"
        ).extract()[0].strip()
        if "报告会" not in title:
            return
        des = response.xpath(
            "//div[@id='listContainer']//text()"
        ).extract()
        text = [title]
        for i in des:
            if i.strip() != "":
                text.append(i.strip())
        description = "".join(text)
        if response.request.url not in URL:
            URL.append(response.request.url)
            item['title'] = title
            # find the lecturer via NER
            item['lecturer'] = []
            lecturer = get_lecturer_nlp(description)
            if lecturer:
                item['lecturer'].append(lecturer)
            lec_time = response.xpath(
                "//p[contains(string(),'时间')]/text()"
            ).extract()
            if len(lec_time) != 0:
                item['lecture_time'] = lec_time[0].strip().replace("报告时间：", "")
            issued_time = response.xpath(
                "//div[@class='info-time']/span/text()"
            ).extract()[0]
            issued_time = issued_time.replace('发布时间：', '')
            item['issued_time'] = issued_time
            loc = response.xpath(
                "//p[contains(string(),'地点')]/text()"
            ).extract()
            if len(loc) != 0:
                for i in loc:
                    if i.strip() == "":
                        continue
                    else:
                        item['location'] = i.strip().replace("报告地点：", "")
                        break
            item['url'] = response.request.url
            item['uni'] = 'SCUT'
            item['description'] = description
            yield item
        return
