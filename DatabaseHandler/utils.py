import time
import json
import requests
import random
import hashlib
from urllib import request

# NLP utils
# XToken = '0Itav5d7.35733.rYTjnGcPDndq'
XToken = '4xSNgD3j.35782.hq6p1cqjBZ-h'

# Baidu access token
AT = '24.186e5f8b30d07cc292e3695145471c70.2592000.1569088021.282335-16860975'

# Baidu Translate
APPID = '20190821000328416'
SECRETEKEY = 'MF3C0GQ5NlqYDKBPKuU_'

KEYWORDS_URL = 'http://api.bosonnlp.com/keywords/analysis'

NER_URL = 'http://api.bosonnlp.com/ner/analysis'

OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"

# check correlation utils
INTERESTED = [
    '密码', 'cryptography', 'cryptographic',
    '密码学', 'information security', 'confidential',
    '信息安全', 'information safety', 'cybersecurity',
]


# check if the lecture is able to be selected
def is_interested(description, interested_words=tuple(INTERESTED), use_nlp=False):
    if interested_words == [""]:
        return True
    if use_nlp:
        params = {'top k': 10}
        data = json.dumps(description)
        headers = {
            'X-Token': XToken,
            'Content-Type': 'application/json'
        }
        resp = requests.post(
            KEYWORDS_URL, headers=headers, params=params, data=data.encode('utf-8')
        )
        for _, word in resp.json():
            if word in interested_words:
                return True
        return False
    else:
        for interest in interested_words:
            if interest in description:
                return True
        return False


def is_wanted_uni(uni, lecture_uni):
    if uni is None or (uni is not None and lecture_uni == uni):
        return True
    else:
        return False


# 如果更改了lecture_time的类型就会报错
def is_wanted_timeslot(start, end, lecture_time):
    t = ""
    if lecture_time is not None and lecture_time != "":
        time_split = str(lecture_time).split('-')
        y = time_split[0]
        m = time_split[1]
        d = time_split[2]
        if len(m) == 1:
            m = '0' + m
        if len(d) == 1:
            d = '0' + d
        t = y + m + d
    if start is not None \
            and start != "" \
            and start \
            > t:
        return False
    if end is not None \
            and end != "" \
            and end \
            < t:
        return False
    return True


def convert_img(url):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {
        'access_token': AT,
        'url': url
    }
    resp = requests.post(OCR_URL, headers=headers, params=params)
    d = resp.json()
    if 'words_result' in d.keys():
        string = d['words_result']
        text = []
        for s in string:
            text.append(s['words'])
        description = "".join(text)
        return description
    else:
        return False


def get_lecturer_nlp(des):
    s = [des]
    data = json.dumps(s)
    headers = {
        'X-Token': XToken,
        'Content-Type': 'application/json'
    }
    resp = requests.post(NER_URL, headers=headers, data=data.encode('utf-8'))
    try:
        for item in resp.json():
            for entity in item['entity']:
                if entity[2] == 'person_name':
                    return ''.join(item['word'][entity[0]:entity[1]])
    except:
        return False


def sort_lectureList(list_to_sort, key):
    outer_index = 0
    for _ in list_to_sort:
        inner_index = outer_index
        while inner_index > 0 \
                and compareTime(list_to_sort[inner_index - 1].get(key, None),
                                list_to_sort[inner_index].get(key, None)):
            temp = list_to_sort[inner_index]
            list_to_sort[inner_index] = list_to_sort[inner_index - 1]
            list_to_sort[inner_index - 1] = temp
            inner_index -= 1
        outer_index += 1
    return


# Translate Chinese keywords into English
def translate(query):
    myurl = '/api/trans/vip/translate'
    q = query
    fromLang = 'zh'
    toLang = 'en'
    salt = random.randint(32768, 65536)

    sign = APPID + q + str(salt) + SECRETEKEY
    m1 = hashlib.md5()
    m1.update(sign.encode(encoding='utf-8'))
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + APPID + '&q=' + request.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    resp = requests.get('http://api.fanyi.baidu.com' + myurl)
    try:
        return resp.json().get('trans_result', None)[0].get('dst', None)
    except:
        return None


def compareTime(t1, t2):
    # str->time
    if t1 is None or t1 == '':
        return True
    if t2 is None or t2 == '':
        return False
    str1 = str(t1)
    str2 = str(t2)
    if not str1[0:4].isdigit():
        return True
    if not str2[0:4].isdigit():
        return False
    if len(str1.strip()) > 10:
        t1 = str1[0:4] + '-'
        t1 = t1 + str1[str1.find('-') + 1:str1.find('-', 6)] + '-'
        if str1[str1.find('-', 6) + 1:str1.find('-', 6) + 3].isdigit():
            t1 = t1 + str1[str1.find('-', 6) + 1:str1.find('-', 6) + 3]
        else:
            t1 = t1 + str1[str1.find('-', 6) + 1:str1.find('-', 6) + 2]
    if len(str2.strip()) > 10:
        t2 = str2[0:4] + '-'
        t2 = t2 + str2[str2.find('-') + 1:str2.find('-', 6)] + '-'
        if str2[str2.find('-', 6) + 1: str2.find('-', 6) + 3].isdigit():
            t2 = t2 + str2[str2.find('-', 6) + 1: str2.find('-', 6) + 3]
        else:
            t2 = t2 + str2[str2.find('-', 6) + 1: str2.find('-', 6) + 2]
    t1_time = time.strptime(t1, '%Y-%m-%d')
    t2_time = time.strptime(t2, '%Y-%m-%d')
    if int(time.strftime('%Y%m%d', t1_time)) > int(time.strftime('%Y%m%d', t2_time)):
        return True
    else:
        return False


if __name__ == "__main__":
    des = """
    报告题目:自然语言理解与认知时间：2018年9月12日10：00地点：大学城B8附楼报告厅报告摘要:虽然自然语言一直在社会、经济和国家安全等领域中扮演着重要角色，但是一直以来计算机的自然语言理解与认知能力远逊于人类。近几年，随着移动互联网的不断普及，以及云计算、大数据、GPU、深度学习等相关平台和技术的快速发展，我们越来越感到自然语言处理方面的突破就在眼前。本报告将从自然语言理解与认知等两个层面探讨如何提高自然语言处理能力。具体包括：自然语言本质特点、语言学理论简介（结构主义语言学、转换生成语法、形式语言学、功能语言学、认知语言学）、自然语言理解基础、自然语言认知基础（认知科学、认知语言学）。讲者简介：周国栋教授1997年12月毕业于新加坡国立大学获得博士学位；1998年1月至1999年3月在新加坡国立大学从事博士后研究；1999年4月-2006年8月在新加坡资讯通信研究院分别担任副研究员、研究员和副主任研究员；2006年8月底加入苏州大学担任教授博导，组建自然语言处理实验室。研究方向：自然语言理解、信息抽取、自然语言认知等。近5年来发表国际著名SCI期刊论文20多篇和国际顶级会议AC
    """
    print(is_interested(des, use_nlp=True))
