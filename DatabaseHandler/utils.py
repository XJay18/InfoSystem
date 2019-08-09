import time
import json
import requests

# NLP utils
XToken = '0Itav5d7.35733.rYTjnGcPDndq'
# 4xSNgD3j.35782.hq6p1cqjBZ-h

# Baidu access token
AT = '24.42307f0713b2249c5ace8160b2e39aac.2592000.1566382436.282335-16860975'

KEYWORDS_URL = 'http://api.bosonnlp.com/keywords/analysis'
NLP_KEYWORDS = False

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
    if use_nlp:
        params = {'top k': 30}
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
                and compareTime(list_to_sort[inner_index - 1][key], list_to_sort[inner_index][key]):
            temp = list_to_sort[inner_index]
            list_to_sort[inner_index] = list_to_sort[inner_index - 1]
            list_to_sort[inner_index - 1] = temp
            inner_index -= 1
        outer_index += 1
    return


def compareTime(t1, t2):
    # str->time
    if t1 is None or t2 is None:
        return False
    t1_time = time.strptime(t1, '%Y-%m-%d')
    t2_time = time.strptime(t2, '%Y-%m-%d')
    if int(time.strftime('%Y%m%d', t1_time)) > int(time.strftime('%Y%m%d', t2_time)):
        return True
    else:
        return False
