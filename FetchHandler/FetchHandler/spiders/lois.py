import scrapy
from ..items import InfoItem
import re

URL = []


class LOIS(scrapy.Spider):
    name = 'lois'
    start_urls = ['http://sklois.iie.cas.cn/xwzx/xshd/index.html']
    n_pages = 3
    for i in range(n_pages - 1):
        start_urls.append("http://sklois.iie.cas.cn/xwzx/xshd/index_" + str(i + 1) + ".html")

    def parse(self, response):
        for href in response.xpath("//ul[@class='news_list margin20']//a/@href"):
            url = "http://sklois.iie.cas.cn/xwzx/xshd" + href.extract()[1:]
            # print("url: "+url)
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = InfoItem()
        title = response.xpath(
            "//head//title/text()"
        ).extract()[0].strip()
        title = title.replace('----信工所信息安全国家重点实验室', '')
        if "学术报告" in title or "学术会议" in title:
            title = title.replace('学术报告：', '')
            des = response.xpath(
                "//div[@class='TRS_Editor']//span//text()"
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
                lecturer = re.findall("报告人：(.*?)时间", description)[0]
                if lecturer != '':
                    item['lecturer'].append(lecturer.replace('报告', ''))
                elif re.findall("Speaker:(.*?)Time", description)[0] != '':
                    item['lecturer'].append(re.findall("Speaker:(.*?)Time", description)[0])
                # find the lecture time via regular expression
                lec_time = re.findall("时间：(.*?)地点", description)[0]
                if lec_time != '':
                    item['lecture_time'] = lec_time.replace('报告', '')
                item['issued_time'] = response.xpath(
                    "//td[contains(string(),'发布时间')]/text()"
                ).extract()[0].split('：')[1]
                # find the location via regular expression
                loc = re.findall("地点：(.*?室)", description)[0]
                if loc != '':
                    item['location'] = loc
                item['url'] = response.request.url
                item['uni'] = 'LOIS'
                item['description'] = description
                yield item
        return
