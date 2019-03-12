# -*_ coding:UTF-8 -*_
import pymongo

"""
建立新集合Collections,包含字段有省份、城市名以及对应所在的Collection的名字

"""

client = pymongo.MongoClient('localhost', 27017)
db = client["HousePriceHistory"] # 连接数据库
collist = db.list_collection_names() # 获取当前数据库下的所有集合
#for i in collist:
#    print(i)
#print(len(collist))
col_insert = db["Collections"]
for col in collist:
    #print(col)
    if col == "A_New":  # 跳过特殊集合
        continue
    results = db.get_collection(col).find({"year": "2019", "month": "03","area":"1"},{"_id":0,"city_name":1,"province":1})
    #print(results)
    #print(results[0]['province'])

    #col_insert.insert_many({"collection_name":col,"province":results.get('province')})
    for doc in results:
        #print(doc)
        print(doc['province'],doc['city_name'])
        col_insert.insert_one({"collection_name":col,"province":doc['province'],"city_name":doc['city_name']})










