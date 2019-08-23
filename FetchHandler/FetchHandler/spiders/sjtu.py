import scrapy
import time
from os.path import dirname
import sys
from ..items import InfoItem

sys.path.append(dirname(dirname(dirname(dirname(__file__)))))
from DatabaseHandler.utils import convert_img, get_lecturer_nlp

URL = []
STATE = "/wEPDwUKMTMxMDcwNDI3OQ9kFgICAQ9kFgQCAQ8PFgIeC1JlY29yZGNvdW" \
        "50AsgBZGQCAg9kFgQCAw8QZBAVAyrmmbrog73orqHnrpfkuI7mmbrog73n" \
        "s7vnu5/ph43ngrnlrp7pqozlrqQ55LiK5rW35biC5pWZ5aeU5pm66IO95L" \
        "qk5LqS5LiO6K6k55+l5bel56iL6YeN54K55a6e6aqM5a6kJOecgemDqOWF" \
        "seW7uuWbveWutumHjeeCueWunumqjOWupOKAphUDAjI3AjY2AjEyFCsDA2" \
        "dnZ2RkAgcPEGQQFQch6auY5Y+v6Z2g6L2v5Lu25LiO55CG6K6656CU56m2" \
        "5omAHuW5tuihjOS4juWIhuW4g+iuoeeul+eglOeptuaJgB7nvZHnu5zkuI" \
        "7mnI3liqHorqHnrpfnoJTnqbbmiYAb5pm66IO95Lq65py65Lqk5LqS56CU" \
        "56m25omAHuWvhueggeS4juS/oeaBr+WuieWFqOeglOeptuaJgBjorqHnrp" \
        "fmnLrlupTnlKjnoJTnqbbmiYAe6K6h566X5py65L2T57O757uT5p6E56CU" \
        "56m25omAFQcBMgExATYBNwE1ATQBMxQrAwdnZ2dnZ2dnZGRk4Zi9HmYEVO" \
        "AwKHOw8Aa4FhW3Wvs="
VALIDATION = "/wEWDwKJor+7BwLlx+GRCQKbg+qIDQLOjMitAgL258r4BALy59b4BAL3" \
             "5+b4BALPjMitAgKdnYvEDgKcnYvEDgKZnYvEDgKanYvEDgKYnYvEDgKf" \
             "nYvEDgKenYvEDlASbLxk18WaekQnSFimdcseIBO6"
FAILED_TIMES_LIMIT = 5


class SJTU(scrapy.Spider):
    name = 'sjtu'

    def start_requests(self):
        n_pages = 3
        for i in range(n_pages):
            post_url = 'http://www.cs.sjtu.edu.cn/NewNotice.aspx'
            formdata = {
                '__EVENTTARGET': 'AspNetPager1',
                '__EVENTARGUMENT': str(i + 1),
                '__VIEWSTATE': STATE,
                '__EVENTVALIDATION': VALIDATION,
                'Top$Textbox': '1',
                'AspNetPager1_input': '1'
            }
            yield scrapy.FormRequest(url=post_url, formdata=formdata, callback=self.parse)

    def parse(self, response):
        for href in response.xpath("//div[@class='NewsList']//a[contains(string(),'讲座')]/@href"):
            url = "http://www.cs.sjtu.edu.cn/" + href.extract()
            # print("url: "+url)
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = InfoItem()

        title = response.xpath(
            "//h2[contains(string(),'讲座')]/text()"
        ).extract()[0].strip()[3:].strip()

        # convert the image from the website
        img_url = response.xpath(
            "//div[@class='p20 lh250']/img/@src"
        ).extract()[0]
        img_url = 'http://www.cs.sjtu.edu.cn' + img_url
        description = convert_img(img_url)
        failed_times = 1
        while not description:
            if failed_times < FAILED_TIMES_LIMIT:
                print("* Failed_times: %d *" % failed_times)
                print("*" * 50)
                # sleep at most 5 secs
                time.sleep(min(1.5 * failed_times, 5))
                failed_times += 1
                print("Start reconverting... ")
                description = convert_img(img_url)
            else:
                # fail to convert img into string
                print("\n###Trouble in converting this lecture news: %s \n" % title)
                return

        if response.request.url not in URL:
            URL.append(response.request.url)
            item['title'] = title
            item['lecturer'] = []
            lecturer = get_lecturer_nlp(description)
            if lecturer:
                item['lecturer'].append(lecturer)
            item['issued_time'] = response.xpath(
                "//div[@class='tc lh300']/text()"
            ).extract()[0].strip()[5:]
            item['url'] = response.request.url
            item['uni'] = 'SJTU'
            item['description'] = description
            yield item
        return
