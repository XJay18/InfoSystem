from flask import Flask, request
from flask import jsonify

from initiation import InfoDB
from utils import is_interested, is_wanted_uni, sort_lectureList, is_wanted_timeslot, translate

app = Flask(__name__)

infoDB = InfoDB()
infoDB.openDB()
SETTINGS = {'use_nlp': False, 'sort_type': 'lec_time'}
WEBSITES = []


# api function
@app.route('/api/getInfo', methods=['GET', 'POST'])
def get_list():
    if request.method == 'GET':
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
                             use_nlp=SETTINGS['use_nlp']):
                lecture_dict = {}
                for key, value in zip(dict_key, lecture_item):
                    if key != 'id' and key != 'description':
                        lecture_dict[key] = value
                result.append(lecture_dict)
        sort_lectureList(result, SETTINGS['sort_type'])
        return jsonify({'data': result, 'keys': dict_key[1:-1]})
    else:
        # type: list
        kwords = request.form.get("keywords").split('|')
        keywords = []
        for k in kwords:
            if k != "":
                keywords.append(k)
            # if is chinese
            if '\u4e00' <= k <= '\u9fff':
                correspond_eng = translate(k)
                if correspond_eng:
                    keywords.append(correspond_eng)
        # empty query condition
        if not keywords:
            keywords.append("")
        uni = request.form.get("uni")
        time_start = request.form.get("time_start")
        time_end = request.form.get("time_end")

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
                             use_nlp=SETTINGS['use_nlp']) \
                    and is_wanted_uni(uni=uni,
                                      lecture_uni=lecture_item[6]) \
                    and is_wanted_timeslot(start=time_start, end=time_end, lecture_time=lecture_item[4]):
                lecture_dict = {}
                for key, value in zip(dict_key, lecture_item):
                    if key != 'id' and key != 'description':
                        lecture_dict[key] = value
                result.append(lecture_dict)
        sort_lectureList(result, SETTINGS['sort_type'])
        return jsonify({'data': result, 'keys': dict_key[1:-1]})


@app.route('/api/getSettings', methods=['GET'])
def get_settings():
    return jsonify(SETTINGS)


@app.route('/api/setSettings', methods=['POST'])
def set_settings():
    sort_type = request.form.get('sort_type')
    SETTINGS.update({'sort_type': sort_type})
    return jsonify(SETTINGS)


@app.route('/api/appendWeb', methods=['GET', 'POST'])
def append_web():
    if request.method == 'GET':
        return jsonify({'webs to append': WEBSITES})
    else:
        WEBSITES.append(request.form.get('website'))
        return jsonify({'status': 'OK'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    infoDB.closeDB()
# host='0.0.0.0', port=5000
