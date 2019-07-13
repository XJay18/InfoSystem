import scrapy
from ..items import InfoItem


class IF_JNU(scrapy.Spider):
    name = 'if_jnu'
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
            item['title'] = response.xpath(
                "//div[@class='conTxt']//p[1]/text()"
            ).extract()
            # print(item['title'])
            item['issuedDate'] = response.xpath(
                "//div[@class='property']//span[3]/text()"
            ).extract()[0].split("：")[1]
            # print(item['issuedDate'])
            item['url'] = response.request.url
            yield item
        else:
            pass
