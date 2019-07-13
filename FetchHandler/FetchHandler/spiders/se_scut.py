import scrapy
from ..items import InfoItem


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
        item['title'] = response.xpath(
            "//div[@class='arti_cont']//h2/text()"
        ).extract()[0].strip()
        # print(item['title'])
        item['issuedDate'] = response.xpath(
            "//span[@class='arti_update']/text()"
        ).extract()[0].split("：")[1]
        # print(item['issuedDate'])
        item['url'] = response.request.url
        yield item
