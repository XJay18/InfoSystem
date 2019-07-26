import scrapy
from ..items import InfoItem

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
            issued_time = response.xpath(
                "//div[@class='NewsDate']//a[@class='putDate']/text()"
            ).extract()[0]
            issued_time = issued_time.replace('年', '-')
            issued_time = issued_time.replace('月', '-')
            item['issued_time'] = issued_time.replace('日', '')
            # print(item['issuedDate'])
            item['url'] = response.request.url
            item['uni'] = 'SCUT'
            item['description'] = description
            yield item
        return
