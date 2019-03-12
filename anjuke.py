# -*_ coding:UTF-8 -*_
import requests
from bs4 import BeautifulSoup

city = "suzhou"
city_name = "苏州"
flag = "1"  # 标志着整个苏州

headers_ = {'User-Agent':'Mozilla/5.0'}
year = 2018
url = 'https://www.anjuke.com/fangjia/suzhou' + str(year) + '/'
#print(url)

req = requests.get(url=url,headers=headers_)
req.encoding = req.apparent_encoding
#print(req.status_code)
html = req.text
req.close()

bf = BeautifulSoup(html,'html.parser')
# clearfix up 上涨 clearfix down 下降 clearfix nochange 不变
"""
lis = bf.find_all('li',class_="clearfix up")
dates = [] #2018年12月房价
prices = [] #16943元/m^2
trendency = [] #1.33%up
for li in lis:
    dates = li.find_all('b')
    prices = li.find_all('span')
    trendency = li.find_all('em')

print(dates[0],prices[0],trendency[0])
"""
div_own = bf.find('div',class_='fjlist-box boxstyle2')
title_own = bf.find('h3',class_='pagemod-tit')
#print(title_own.text)

dates = div_own.find_all('b')
#print(dates[0].text)
prices = div_own.find_all('span')
#print(prices[0].text)
trendency = div_own.find_all('em')
#print(trendency[1].text)

print(title_own.text)
for i in range(len(dates)):  #迭代不能直接用int类型，加一个range
    print(dates[i].text,"  ",prices[i].text,"  ",trendency[i].text)
    #print(dates[i].text[0:4],"  ",dates[i].text[5:7])


import pymongo
client = pymongo.MongoClient('localhost',27017)
db = client["HousePriceHistory"]
collist = db.list_collection_names()
col = db["suzhou"]
if "suzhou" in collist:
    db.drop_collection(col)

for i in range(len(dates)):
    dict_final = {"city_name":city_name,"area":flag,"year":dates[i].text[0:4],"month":dates[i].text[5:7],
                  "price":prices[i].text,"trendency":trendency[i].text}
    x = col.insert_one(dict_final)
