from flask import Flask, request, Response

from DatabaseHandler.initiation import InfoDB
from DatabaseHandler import utils

app = Flask(__name__)


# def get_dict():
#     result = list(CUR.execute('select * from Lecture'))
#     return result

infoDB = InfoDB()

IS_NLP = False
SORT_INDEX = 'issued_time'


# api function
@app.route('/api/getInfo', methods=['GET', 'POST'])
def get_list():
    if request.method == 'GET':
        infoDB.openDB()
        result = infoDB.get_Lecture_Datadict()
        infoDB.closeDB()
        #
        # dict_key = [
        #     'id',
        #     'lec_title',
        #     'lecturer',
        #     'issued_time',
        #     'lec_time',
        #     'loc',
        #     'uni',
        #     'url',
        #     'description']
        # for row in datalist:
        #     element_of_list = {}
        #     i = 0
        #     for element in row:
        #         if element and i != 0:
        #             element_of_list[dict_key[i]] = element
        #         i += 1
        #     list_of_dict.append(element_of_list)
        return {'data': result[0], 'keys': result[1]}
    else:
        result = []
        dict_key = [
            'id',
            'title',
            'lecturer',
            'issued_time',
            'lecture_time',
            'loc',
            'uni',
            'url',
            'description']
        infoDB.openDB()
        for lecture_item in infoDB.get_Lecture_Datalist():
            if utils.is_interested(description=lecture_item[8], use_nlp=IS_NLP):
                lecture_dict = {}
                for key, value in zip(dict_key, lecture_item):
                    lecture_dict[key] = value
                result.append(lecture_dict)
        utils.sort_lectureList(result, SORT_INDEX)
        infoDB.closeDB()
        return {'data': result, 'keys': dict_key[1:]}


if __name__ == "__main__":
    app.run()
# host='0.0.0.0', port=5000