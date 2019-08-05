from flask import Flask, request, Response
import os
import sqlite3

app = Flask(__name__)
DATABASE = os.path.join(
    os.path.dirname(__file__), 'info_database.sqlite'
)

# set up connection to DB
CONN = sqlite3.connect(DATABASE)
CUR = CONN.cursor()


def get_dict():
    result = list(CUR.execute('select * from Lecture'))
    return result

# api function
@app.route('/api/getInfo', methods=['GET', 'POST'])
def get_list():
    if request.method == 'GET':
        datalist = get_dict()
        list_of_dict = []
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
        for row in datalist:
            element_of_list = {}
            i = 0
            for element in row:
                if element and i != 0:
                    element_of_list[dict_key[i]] = element
                i += 1
            list_of_dict.append(element_of_list)
        return {'data': list_of_dict, 'keys': dict_key[1:]}
    else:
        # TODO: complete the function with query keys as input
        return Response("Not Implemented.", 500,
                        mimetype='application/text')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
