# ==============================================================================
# Initiate the sqlite database, create tables for future use.
# ==============================================================================

import sqlite3
import json


class InfoDB:
    def openDB(self):
        self.conn = sqlite3.connect('info_database.sqlite')
        self.cursor = self.conn.cursor()

    def closeDB(self):
        self.conn.close()

    def create_table(self):
        #autoincrement要是integer才可以
        create_statement1 = '''create table Lecture (
            lecture_ID integer primary key autoincrement,
            title text,
            issuedDate text,
            holdingDate text,
            place text,
            uni text,
            url text,
            foreign key (uni) references College(uni)
        )'''
        create_statement2 = '''create table Lecturer(
            lecture_ID int,
            name text,
            primary key(lecture_ID,name),
            foreign key (lecture_ID) references Lecture(lecture_ID)
        ) 
        '''
        create_statement3 = '''create table College(
            uni text primary key,
            college_url text
        )
        '''
        create_statement4 = '''create table User(
            user_name text primary key,
            user_pwd text
        )
        '''

        self.cursor.execute(create_statement1)
        self.cursor.execute(create_statement2)
        self.cursor.execute(create_statement3)
        self.cursor.execute(create_statement4)
        self.conn.commit()


    def insert_College(self,uni,college_url):
        '向College表插入行'
        stm='''insert into College values(?,?)'''
        self.cursor.execute(stm,(uni,college_url))
        self.conn.commit()


    def insert_Lecture(self,title='',issuedDate='',holdingDate='',place='', uni='' ,url=''):
        '向Lecture表插入行'
        #lecture_ID自增
        stm='''insert into Lecture(title,issuedDate,holdingDate,place, uni ,url) values(
            ?,?,?,?,?,?)'''
        self.cursor.execute(stm,(title,issuedDate,holdingDate,place, uni ,url))
        self.conn.commit()

    def insert_Lecturer(self,lecture_ID ,name):
        '向College表插入行'
        stm='''insert into Lecturer values(?,?)'''
        self.cursor.execute(stm,(lecture_ID ,name))
        self.conn.commit()    

    def insert_User(self,user_name,user_pwd):
        stm='''insert into User values(
            {},{})'''.format(user_name,user_pwd)
        self.cursor.execute(stm)
        self.conn.commit()
    def getConn(self):
        return self.conn
    def getCursor(self):
        return self.cursor
def test():
    data=read_json()
    #打开sqlite
    infodb=InfoDB()
    infodb.openDB()
    #infodb.create_table()
    #infodb.insert_College('SCUT','www.scut.edu.cn')
    for item in data:
        infodb.insert_Lecture(title=item['title'],url=item['url'],issuedDate=item['issuedDate'])
    for i in infodb.getCursor().execute('select * from Lecture'):
        print(i)
    infodb.closeDB()


def read_json():
    with open(r'E:\Projects\数据库实训-学术讲座爬虫\InfoSystem\FetchHandler\scut.json','r') as json_data:
        data=json.load(json_data)
        return data
            
# read_json()
# if __name__=='__main__':test()

info=InfoDB()
info.openDB()
data=read_json()
for item in info.getCursor().execute('select * from Lecture'):
    print(item)

info.getConn().commit()
info.closeDB()
