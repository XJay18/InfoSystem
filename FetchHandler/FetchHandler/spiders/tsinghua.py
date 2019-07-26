import scrapy
from ..items import InfoItem
from ..utils import is_interested

URL = []


class TH(scrapy.Spider):
    name = 'th'
    start_urls = []
    n_pages = 3
    for i in range(n_pages):
        start_urls.append("http://iiis.tsinghua.edu.cn/list-265-" + str(i + 1) + ".html")

    def parse(self, response):
        for href in response.xpath("//table[@class='table table-striped']//a/@href"):
            url = "http://iiis.tsinghua.edu.cn" + href.extract()
            # print("url: "+url)
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = InfoItem()
        con = response.xpath("//p[contains(string(),'标题')]/text()").extract()
        content = []
        for i in con:
            if i.strip() == '':
                continue
            else:
                content.append(i.strip())
        title = content[0]
        des = response.xpath(
            "//div[@class='contentss']//text()"
        ).extract()
        text = [title]
        for i in des:
            if i.strip() != "":
                text.append(i.strip())
        description = "".join(text)
        if response.request.url not in URL:
            URL.append(response.request.url)
            item['title'] = title
            item['lecturer'] = content[1]
            # Because there are not any issued time we can get from the websites,
            # we assume the issued time is the same as the lecture time.
            item['issued_time'] = content[2][0:10]
            item['lecture_time'] = content[2]
            item['location'] = content[3]
            item['url'] = response.request.url
            item['uni'] = 'TSINGHUA'
            item['description'] = description
            yield item
        return
