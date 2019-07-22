import json
import requests

# NLP utils
XToken = '0Itav5d7.35733.rYTjnGcPDndq'

KEYWORDS_URL = 'http://api.bosonnlp.com/keywords/analysis'
NLP_KEYWORDS = False

NER_URL = 'http://api.bosonnlp.com/ner/analysis'

# check correlation utils
INTERESTED = [
    '密码', 'cryptography',
    '密码学', 'information security',
    '信息安全', 'information safety',
]


# check if the lecture is able to be selected
def is_interested(description, use_nlp=False):
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
            if word in INTERESTED:
                return True, word
        return False
    else:
        for interest in INTERESTED:
            if interest in description:
                return True, interest
        return False
