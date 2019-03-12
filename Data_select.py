# -*_ coding:UTF-8 -*_
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client["HousePriceHistory"] # 连接数据库
collist = db.list_collection_names() # 获取当前数据库下的所有集合
#for i in collist:
#    print(i)
#print(len(collist))
col_insert = db["A_New"]
for col in collist:
    #print(col)
    results = db.get_collection(col).find({"year": "2019", "month": "03"})
    col_insert.insert_many(results)
    #for doc in results:
    #    print(doc)
    #    col_insert.insert_one(doc)










