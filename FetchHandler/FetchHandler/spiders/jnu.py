import scrapy
from ..items import InfoItem

URL = []


class IF_JNU(scrapy.Spider):
    name = 'jnu'
    start_urls = []
    n_pages = 3

    for i in range(n_pages):
        start_urls.append("https://xxxy2016.jnu.edu.cn/Category_37/Index_" + str(i + 1) + ".aspx")

    def parse(self, response):
        for href in response.xpath("//ul[contains(@class,'newsList')]//a/@href"):
            url = "https://xxxy2016.jnu.edu.cn" + href.extract()
            # print("url: "+url)
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = InfoItem()
        myfilter = response.xpath(
            "//div[@class='articleCon']//h2/text()"
        ).extract()[0]
        if "学术讲座" in myfilter:
            try:
                title = response.xpath(
                    "//div[@class='conTxt']//p[1]/text()"
                ).extract()[0]
            except IndexError:
                return
            if title == '\xa0':
                title = response.xpath(
                    "//h2[@class='title']/text()"
                ).extract()[0]
            des = response.xpath(
                "//div[@id='fontzoom']//text()"
            ).extract()
            text = [title]
            for i in des:
                if i.strip() != "":
                    text.append(i.strip())
            description = "".join(text)
            if response.request.url not in URL:
                URL.append(response.request.url)
                item['title'] = title
                lecturers = response.xpath(
                    "//p[contains(string(),'报告人：')]/text()"
                ).extract()
                item['lecturer'] = []
                for lecturer in lecturers:
                    item['lecturer'].append(lecturer.strip())
                lec_time = response.xpath(
                    "//p[contains(string(),'时') and contains(string(),'间：')]/text()"
                ).extract()
                if len(lec_time) != 0:
                    item['lecture_time'] = lec_time[0].strip().replace("始", "")
                issued_time = response.xpath(
                    "//div[@class='property']//span[3]/text()"
                ).extract()[0].split("：")[1]
                issued_time = issued_time.replace('年', '-')
                issued_time = issued_time.replace('月', '-')
                item['issued_time'] = issued_time.replace('日', '')
                loc = response.xpath(
                    "//p[contains(string(),'地') and contains(string(),'点：')]/text()"
                ).extract()
                if len(loc) != 0:
                    item['location'] = loc[0].strip()
                item['url'] = response.request.url
                item['uni'] = 'JNU'
                item['description'] = description
                yield item
        return
