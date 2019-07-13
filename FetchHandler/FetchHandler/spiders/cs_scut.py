import scrapy
from ..items import InfoItem


class CS_SCUT(scrapy.Spider):
    name = 'cs_scut'
    start_urls = []
    n_pages = 3
    for i in range(n_pages):
        start_urls.append(
            "http://cs.scut.edu.cn/newcs/xygk/xytz/index.html?_page_=%d" % (i + 1)
        )

    def parse(self, response):
        for href in response.xpath("//a[@class='LTitle']/@href"):
            if "https://" not in href.extract():
                url = "http://cs.scut.edu.cn" + href.extract()
                yield scrapy.Request(url, callback=self.parse_dir_contents)

            # not in school of cs
            else:
                pass
            # print("url: " + url)

    def parse_dir_contents(self, response):
        item = InfoItem()
        item['title'] = response.xpath(
            "//div[@class='NewsTitle']/text()"
        ).extract()[0].strip()
        # print(item['title'])
        item['issuedDate'] = response.xpath(
            "//div[@class='NewsDate']//a[@class='putDate']/text()"
        ).extract()[0]
        # print(item['issuedDate'])
        item['url'] = response.request.url
        yield item
