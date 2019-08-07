from DatabaseHandler.initiation import InfoDB
from DatabaseHandler import utils


# infoDB = InfoDB()
# SORT_INDEX = 'issued_time'
# result = []
# dict_key = [
#             'id',
#             'title',
#             'lecturer',
#             'issued_time',
#             'lecture_time',
#             'loc',
#             'uni',
#             'url',
#             'description']
# infoDB.openDB()
# for lecture_item in infoDB.get_Lecture_Datalist():
#             if utils.is_interested(description=lecture_item[8], use_nlp=False):
#                 lecture_dict = {}
#                 for key, value in zip(dict_key, lecture_item):
#                     lecture_dict[key] = value
#                 result.append(lecture_dict)
# utils.sort_lectureList(result, SORT_INDEX)
# infoDB.closeDB()
# for item in result:
#     print(item)

# 表的内容
test_db = InfoDB()
test_db.openDB()
result, dict_index = test_db.get_Lecture_Datadict()
utils.sort_lectureList(result, 'issued_time')
for item in result:
    print(item)





# create table if not exists timecmp(
#     id integer primary key,
#     time timestamp NOT NULL DEFAULT (datetime('now','localtime'))
# )
# '''
# insert into timecmp values(
#     6,'2019-9-3 00:06:33'
# )
# stm="select * from timecmp where time > '2019-07-31 00:36:45' "


