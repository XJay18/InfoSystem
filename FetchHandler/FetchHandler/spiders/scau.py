import scrapy
from ..items import InfoItem
import re

URL = []


class SCAU(scrapy.Spider):
    name = 'scau'
    start_urls = []
    n_pages = 3
    for i in range(n_pages):
        start_urls.append("http://info.scau.edu.cn/3762/list" + str(i + 1) + ".htm")

    def parse(self, response):
        for href in response.xpath("//td[@style='text-align:left']/a/@href"):
            url = "http://info.scau.edu.cn" + href.extract()
            # print("url: "+url)
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = InfoItem()
        title = response.xpath(
            "//head//title/text()"
        ).extract()[0].strip()
        des = response.xpath(
            "//div[@class='wp_articlecontent']//text()"
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
            lecturer = re.findall("报告人(.*?)时.?间", description)
            if len(lecturer) != 0:
                item['lecturer'].append(lecturer[0].replace(":", "").replace("：", ""))
            # find the lecture time via regular expression
            lec_time = re.findall("(20.*?)地.?点", description)
            if len(lec_time) != 0:
                item['lecture_time'] = lec_time[0]
            item['issued_time'] = response.xpath(
                "//span[contains(string(),'发布时间')]/text()"
            ).extract()[0].split(':')[1]
            # find the location via regular expression
            loc = re.findall("地.?点(.*?)联系人", description)
            if len(loc) != 0:
                item['location'] = loc[0].replace(":", "").replace("：", "")
            item['url'] = response.request.url
            item['uni'] = 'SCAU'
            item['description'] = description
            yield item
        return
