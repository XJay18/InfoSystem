from initiation import InfoDB

#To initial table 'College'


infodb=InfoDB()
infodb.openDB('E:\Projects\数据库实训-学术讲座爬虫\InfoSystem\FetchHandler\FetchHandler\spiders')
for item in infodb.getCursor().execute('select * from Lecture'):   
    print(item)
infodb.closeDB()