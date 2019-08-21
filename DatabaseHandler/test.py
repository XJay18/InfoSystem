from DatabaseHandler.initiation import InfoDB

infoDB = InfoDB()
infoDB.openDB()
# for item in infoDB.get_Lecture_Datalist():
#     print(item)
infoDB.getCursor().execute("delete from Lecture where uni='SCAU'")
infoDB.getConn().commit()
infoDB.closeDB()