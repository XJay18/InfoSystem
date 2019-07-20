import scrapy
from ..items import InfoItem


class PKU(scrapy.Spider):
    name = 'pku'
    start_urls = ['http://eecs.pku.edu.cn/xygk1/jzxx1.htm']

    # n_pages = 3

    # for i in range(n_pages):
    #     start_urls.append("http://info.scau.edu.cn/3762/list" + str(i + 1) + ".htm")

    def parse(self, response):
        second_index = response.xpath("//a[contains(string(),'下一页')]/@href").extract()[0].split('/')[1][0]
        print("*" * 80)
        print(second_index)
        print("*" * 80)
        url = []
        for i in range(3):
            if i == 0:
                url.append(response.request.url)
            else:
                href = 'http://eecs.pku.edu.cn/xygk1/jzxx1/' + str(int(second_index) - i + 1) + '.htm'
                url.append(href)
        for i in url:
            print("*" * 80)
            print(i)
            print("*" * 80)
            yield scrapy.Request(i, callback=self.parse_utils)

    def parse_utils(self, response):
        for href in response.xpath("//a[@class='hvr-shutter-out-vertical']/@href").extract():
            if href[0:5] == '../..':
                href = href[5:]
            elif href[0:2] == '..':
                href = href[2:]
            url = 'http://eecs.pku.edu.cn' + href
            yield scrapy.Request(url, self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = InfoItem()
        item['title'] = response.xpath(
            "//head//title/text()"
        ).extract()[0].strip().split("-")[0]
        # print(item['title'])
        item['issued_time'] = response.xpath(
            "//p[contains(string(),'发布时间')]/text()"
        ).extract()[0].split('：')[1]
        item['url'] = response.request.url
        item['uni'] = 'PKU'
        yield item
