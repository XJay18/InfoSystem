# ==============================================================================
# Initiate the sqlite database, create tables for future use.
# ==============================================================================

import sqlite3
import json
import os


class InfoDB:
    # InfoDB是专门用于管理学校讲座信息的数据库类，有如下功能：
    # 1.使用前要openDB，使用后要closeDB
    # 2.直接插入University，Lecture，Lecturer，User
    # 3.获取University，Lecture，Lecturer，User所有行
    def openDB(self, path=''):
        if path:
            # print('if path')
            self.conn = sqlite3.connect(path + '/' + 'info_database.sqlite')
        else:
            # print('else path')
            self.conn = sqlite3.connect(os.path.dirname(__file__) + '/info_database.sqlite')
        self.cursor = self.conn.cursor()

    def closeDB(self):
        self.conn.close()

    def insert_University(self, uni, uni_url):
        '向College表插入行'
        stm = '''insert into University values(?,?)'''
        self.cursor.execute(stm, (uni, uni_url))
        self.conn.commit()

    def insert_Lecture(self, title, lecturer, issued_time, lecture_time, location, uni, url, description):
        '向Lecture表插入行'
        # lecture_ID自增
        stm = '''insert into Lecture(title, lecturer,issued_time, lecture_time, location, uni ,url,description) values(
            ?,?,?,?,?,?,?,?)'''
        self.cursor.execute(stm,
                            (title,
                             lecturer,
                             issued_time,
                             lecture_time,
                             location,
                             uni,
                             url,
                             description)
                            )
        self.conn.commit()

    def insert_User(self, user_name, user_pwd):
        stm = '''insert into User values(
            {},{})'''.format(user_name, user_pwd)
        self.cursor.execute(stm)
        self.conn.commit()

    def get_Lecture_Datalist(self):
        '''
        return table:lecture all rows(list type)
        '''
        result = list(self.cursor.execute('select * from Lecture'))
        return result

    def get_Lecture_Datadict(self):
        '''
        return table:lecture all rows(list type,element is dict),table:lecture attribute(list type)
        '''
        lecture_all_rows = self.get_Lecture_Datalist()
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
        for row in lecture_all_rows:
            element_of_list = {}
            i = 0
            for element in row:
                if element and i != 0:
                    element_of_list[dict_key[i]] = element
                i += 1
            list_of_dict.append(element_of_list)
        return list_of_dict, dict_key[1:]

    def get_User_Datalist(self):
        '''
        return table:user all rows(type list)
        '''
        return list(self.cursor.execute('select * from user'))

    def get_User_Datadict(self):
        '''
        return table:user(type list,element dict)
        '''
        user_all_rows = self.get_User_Datalist()
        list_of_dict = []
        user_dict = {}
        for row in user_all_rows:
            user_dict['user_name'] = row[0]
            user_dict['user_pwd'] = row[1]
            list_of_dict.append(user_dict)
        return list_of_dict

    def get_University_datalist(self):
        return list(self.cursor.execute('select * from University'))

    def get_University_datadict(self):
        university_all_rows = self.get_University_datalist()
        list_of_dict = []
        university_dict = {}
        for row in university_all_rows:
            university_dict['uni'] = row[0]
            university_dict['url'] = row[1]
            list_of_dict.append(university_dict)
        return list_of_dict

    def getConn(self):
        return self.conn

    def getCursor(self):
        return self.cursor


# def test():
#     data=read_json()
#     #打开sqlite
#     infodb=InfoDB()
#     infodb.openDB()
#     #infodb.create_table()
#     #infodb.insert_College('SCUT','www.scut.edu.cn')
#     for item in data:
#         infodb.insert_Lecture(title=item['title'],url=item['url'],issued_time=item['issued_time'])
#     for i in infodb.getCursor().execute('select * from Lecture'):
#         print(i)
#     infodb.closeDB()


# def read_json():
#     with open(r'E:\Projects\数据库实训-学术讲座爬虫\InfoSystem\FetchHandler\scut.json','r') as json_data:
#         data=json.load(json_data)
#         return data

def addUniversity():
    infodb = InfoDB()
    infodb.openDB()
    College_name = ['SCUT', 'JUN', 'LOIS', 'PKU', 'SCAU', 'SJTU', 'TSINGHUA']
    College_url = ['', '', '', '', '', '', '']
    db_names = infodb.getCursor().execute('select * from University')
    for name, url in zip(College_name, College_url):
        if (name, url) not in db_names:
            infodb.insert_University(name, url)
    infodb.closeDB()


def create_table():
    infodb = InfoDB()
    infodb.openDB()
    # autoincrement要是integer才可以
    create_statement1 = '''create table if not exists Lecture(
            id integer primary key autoincrement,
            title text,
            lecturer text,
            issued_time text,
            lecture_time text,
            location text,
            uni text,
            url text,
            description text,
            foreign key (uni) references University(uni)
        )'''
    create_statement3 = '''create table if not exists University(
            uni text primary key,
            uni_url text
        )
        '''
    create_statement4 = '''create table if not exists User(
            user_name text primary key,
            user_pwd text
        )
        '''
    infodb.getCursor().execute(create_statement1)
    infodb.getCursor().execute(create_statement3)
    infodb.getCursor().execute(create_statement4)
    infodb.getConn().commit()


create_table()
addUniversity()
