import scrapy
from ..items import InfoItem
import re

URL = []


class CS_SCUT(scrapy.Spider):
    name = 'cs_scut'
    start_urls = []
    n_pages = 3
    for i in range(n_pages):
        start_urls.append(
            "http://cs.scut.edu.cn/newcs/xygk/xytz/index.html" +
            "?__active_paging__=listContainer&_page_=" + str(i + 1) +
            "&__active_region__=pageregion&_size_=15&_=1564021742384"
        )

    def parse(self, response):
        for href in response.xpath("//a[@class='LTitle']/@href"):
            if "http://" not in href.extract() and "https://" not in href.extract():
                url = "http://cs.scut.edu.cn" + href.extract()
                yield scrapy.Request(url, callback=self.parse_dir_contents)
            # not in school of cs
            else:
                return

    def parse_dir_contents(self, response):
        item = InfoItem()
        title = response.xpath(
            "//div[@class='NewsTitle']/text()"
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
            # find the lecturer via regular expression
            item['lecturer'] = []
            lecturer = re.findall("报.?告.?人：(.*?)报告", description)
            if len(lecturer) != 0:
                item['lecturer'].append(lecturer[0])
            lec_time = response.xpath(
                "//p[contains(string(),'时间')]/text()"
            ).extract()
            if len(lec_time) != 0:
                item['lecture_time'] = lec_time[0].strip().replace("报告时间：", "")
            issued_time = response.xpath(
                "//div[@class='NewsDate']//a[@class='putDate']/text()"
            ).extract()[0]
            issued_time = issued_time.replace('年', '-')
            issued_time = issued_time.replace('月', '-')
            item['issued_time'] = issued_time.replace('日', '')
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
