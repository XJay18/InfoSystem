import scrapy
from ..items import InfoItem
from ..utils import is_interested

URL = []


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

        # check if the lecture is able to be selected
        title = response.xpath(
            "//div[@class='arti_cont']//h2/text()"
        ).extract()[0].strip()
        description = response.xpath(
            "//meta[@name='description']/@content"
        ).extract()[0].strip()
        description = "\n".join([title, description])
        if is_interested(description.lower()) and response.request.url not in URL:
            # interested
            URL.append(response.request.url)
            item['title'] = title
            item['issued_time'] = response.xpath(
                "//span[@class='arti_update']/text()"
            ).extract()[0].split("：")[1]
            item['url'] = response.request.url
            item['uni'] = 'SCUT'
            yield item

        # not interested
        print("title: %s not interested." % title)
        
        # 作为数据库的测试
        URL.append(response.request.url)
        item['title'] = title
        item['issued_time'] = response.xpath(
            "//span[@class='arti_update']/text()"
        ).extract()[0].split("：")[1]
        item['url'] = response.request.url
        item['uni'] = 'SCUT'
        yield item
        # # 
        return
