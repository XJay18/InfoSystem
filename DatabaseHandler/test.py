import initiation

test_db = initiation.InfoDB()
test_db.openDB()
print('d')
print(test_db.get_Lecture_Datadict())
# conn=sqlite3.connect('test.db')
# cursor=conn.cursor()
# create_stm = '''
# create table if not exists timecmp(
#     id integer primary key,
#     time timestamp NOT NULL DEFAULT (datetime('now','localtime'))
# )
# '''

# insert_stm='''
# insert into timecmp values(
#     6,'2019-9-3 00:06:33'
# )
# '''
# # cursor.execute(create_stm)
# cursor.execute(insert_stm)
# conn.commit()
# stm="select * from timecmp where time > '2019-07-31 00:36:45' "
# stm_all="select * from timecmp"
# print(list(cursor.execute(stm)))

