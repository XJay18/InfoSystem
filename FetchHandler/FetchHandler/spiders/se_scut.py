import scrapy


class SE_SCUT(scrapy.Spider):
    name = 'se_scut'
    allowed_domains = ["scut.edu.cn/sse/"]
    start_urls = [
        "http://www2.scut.edu.cn/sse/xshd/list.htm",
    ]

    def parse(self, response):
        titles = []
        for title in response.xpath("//ul[contains(@class,'news_ul')]/li[contains(@class,'news_li')]//a//@title"):
            titles.append(title.extract())
            print(title)
        # print(titles)
