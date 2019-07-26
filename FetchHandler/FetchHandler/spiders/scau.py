import scrapy
from ..items import InfoItem

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
            item['issued_time'] = response.xpath(
                "//span[contains(string(),'发布时间')]/text()"
            ).extract()[0].split(':')[1]
            item['url'] = response.request.url
            item['uni'] = 'SCAU'
            item['description'] = description
            yield item
        return
