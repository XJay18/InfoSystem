from initiation import InfoDB

#To initial table 'College'


infodb=InfoDB()
infodb.openDB()
print('ok')
# for item in infodb.getCursor().execute('select * from Lecture'):   
#     print(item)
print(infodb.get_Lecture_Datadict())
infodb.closeDB()