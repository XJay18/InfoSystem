# ==============================================================================
# Initiate the sqlite database, create tables for future use.
# ==============================================================================

import sqlite3


class InfoDB:
    def openDB(self):
        self.conn = sqlite3.connect('info_database.sqlite')
        self.cursor = self.conn.cursor()

    def closeDB(self):
        self.conn.close()

    def create_table(self):
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

    def insert_Lecture(self,lecture_ID ,title,issuedDate,holdingDate,place, uni ,url):
        '向Lecture表插入行'
        stm='''insert into Lecture values(
            {},{},{},{},{},{},{}
            )'''.format(lecture_ID ,title,issuedDate,holdingDate,place, uni ,url)
        self.cursor.execute(stm)
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
    infodb=InfoDB()
    infodb.openDB()
    infodb.create_table()
    infodb.insert_College('Beijing','www.beijing.edu.cn')
    infodb.insert_College('SCUT','www.scut.edu.cn')
    infodb.getCursor().execute('select * from College')
    for i in range(0,2):
        print(infodb.getCursor().fetchone())
    infodb.closeDB()
if __name__=='__main__':test()