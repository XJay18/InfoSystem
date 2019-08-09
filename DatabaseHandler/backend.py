from flask import Flask, request, Response

from initiation import InfoDB
from utils import is_interested, is_wanted_uni, sort_lectureList

app = Flask(__name__)

infoDB = InfoDB()
infoDB.openDB()
IS_NLP = False
SORT_INDEX = 'issued_time'


# api function
@app.route('/api/getInfo', methods=['GET', 'POST'])
def get_list():
    if request.method == 'GET':
        results, keys = infoDB.get_Lecture_Datadict()
        sort_lectureList(results, SORT_INDEX)
        return {'data': results, 'keys': keys}
    else:
        # type: list
        kwords = request.form.get("keywords").split('|')
        keywords = []
        for k in kwords:
            if k != "":
                keywords.append(k)
        # empty query condition
        if not keywords:
            keywords.append("")

        uni = request.form.get("uni")
        result = []
        dict_key = [
            'id',
            'lec_title',
            'lecturer',
            'issued_time',
            'lec_time',
            'loc',
            'uni',
            'url',
            'description']
        for lecture_item in infoDB.get_Lecture_Datalist():
            if is_interested(description=lecture_item[8],
                             interested_words=keywords,
                             use_nlp=IS_NLP) \
                    and is_wanted_uni(uni=uni,
                                      lecture_uni=lecture_item[6]):
                lecture_dict = {}
                for key, value in zip(dict_key, lecture_item):
                    if key != 'id' and key != 'description':
                        lecture_dict[key] = value
                result.append(lecture_dict)
        sort_lectureList(result, SORT_INDEX)
        return {'data': result, 'keys': dict_key[1:-1]}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    infoDB.closeDB()
# host='0.0.0.0', port=5000
