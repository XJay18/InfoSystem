# ==============================================================================
# Initiate the sqlite database, create tables for future use.
# ==============================================================================

import sqlite3
import json
import os

class InfoDB:
    def openDB(self,path=''):
        if path:
            print('if path')
            self.conn = sqlite3.connect(path+'/'+'info_database.sqlite')
        else:
            print('else path')
            self.conn = sqlite3.connect(os.path.dirname(__file__)+'/info_database.sqlite')
        self.cursor = self.conn.cursor()

    def closeDB(self):
        self.conn.close()

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

    def get_Lecture_Datalist(self):
        result=list(self.cursor.execute('select * from Lecture'))
        return result

    def get_Lecture_Datadict(self):
        datalist = self.get_Lecture_Datalist()
        list_of_dict=[]
        index_dict={0:'Lecture_ID',1:'title',2:'issuedtime',\
        3:'holdingDate',4:'place',5:'uni',6:'url'}
        for row in datalist:
            element_of_list={}
            i=0
            for element in row:
                if element:element_of_list[index_dict[i]]=element
                i+=1
            list_of_dict.append(element_of_list)    
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
#         infodb.insert_Lecture(title=item['title'],url=item['url'],issuedDate=item['issuedDate'])
#     for i in infodb.getCursor().execute('select * from Lecture'):
#         print(i)
#     infodb.closeDB()


# def read_json():
#     with open(r'E:\Projects\数据库实训-学术讲座爬虫\InfoSystem\FetchHandler\scut.json','r') as json_data:
#         data=json.load(json_data)
#         return data

def AddCollege():
    infodb=InfoDB()
    infodb.openDB()

    College_name=['SCUT','JUN','LOIS','PKU','SCAU','SJTU','TSINGHUA']
    College_url=['','','','','','','']

    db_names=infodb.getCursor().execute('select * from College')

    for name,url in zip(College_name,College_url):
        if (name,url) not in db_names:
            infodb.insert_College(name,url) 
    infodb.closeDB()            

def create_table():
        infodb=InfoDB()
        infodb.openDB()
        #autoincrement要是integer才可以
        create_statement1 = '''create table if not exists Lecture (
            lecture_ID integer primary key autoincrement,
            title text,
            issuedDate text,
            holdingDate text,
            place text,
            uni text,
            url text,
            foreign key (uni) references College(uni)
        )'''
        create_statement2 = '''create table if not exists Lecturer(
            lecture_ID integer,
            name text,
            primary key(lecture_ID,name),
            foreign key (lecture_ID) references Lecture(lecture_ID)
        ) 
        '''
        create_statement3 = '''create table if not exists College(
            uni text primary key,
            college_url text
        )
        '''
        create_statement4 = '''create table if not exists User(
            user_name text primary key,
            user_pwd text
        )
        '''
        infodb.getCursor().execute(create_statement1)
        infodb.getCursor().execute(create_statement2)
        infodb.getCursor().execute(create_statement3)
        infodb.getCursor().execute(create_statement4)
        infodb.getConn().commit()

create_table()
AddCollege()