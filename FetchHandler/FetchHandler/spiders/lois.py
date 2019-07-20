import scrapy
from ..items import InfoItem


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
        item['title'] = response.xpath(
            "//head//title/text()"
        ).extract()[0].strip()
        item['title'] = item['title'].replace('----信工所信息安全国家重点实验室', '')
        # print(item['title'])
        item['issued_time'] = response.xpath(
            "//td[contains(string(),'发布时间')]/text()"
        ).extract()[0].split('：')[1]
        item['url'] = response.request.url
        item['uni'] = 'LOIS'
        yield item
