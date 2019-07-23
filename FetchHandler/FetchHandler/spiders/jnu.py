import scrapy
from ..items import InfoItem
from ..utils import is_interested

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

            # check if the lecture is able to be selected
            title = response.xpath(
                "//div[@class='conTxt']//p[1]/text()"
            ).extract()[0]
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
            if is_interested(description.lower()) and response.request.url not in URL:
                # interested
                URL.append(response.request.url)
                item['title'] = title
                issued_time = response.xpath(
                    "//div[@class='property']//span[3]/text()"
                ).extract()[0].split("：")[1]
                issued_time = issued_time.replace('年', '-')
                issued_time = issued_time.replace('月', '-')
                item['issued_time'] = issued_time.replace('日', '')
                item['url'] = response.request.url
                item['uni'] = 'JNU'
                yield item

            # not interested
            print("title: %s not interested." % title)
            return
        else:
            print("title: %s not about academic lecture." % myfilter)
            return
