# -*_ coding:UTF-8 -*_
import requests
from bs4 import BeautifulSoup
import random
import pymongo

# 只要更改city和city_name的值
city  = "suzhou"
city_name = "苏州"

def get_area(): # 获取城市所属区的相关信息：网址url+区域名称
    headers = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

    url = 'https://www.anjuke.com/fangjia/'+city+'2018'
    req = requests.get(url=url, headers=headers[random.randint(0,2)])
    req.encoding = req.apparent_encoding
    html = req.text
    req.close()
    bf = BeautifulSoup(html, 'html.parser')
    div = bf.find('div',class_='items')
    areas = div.find_all('a')
    names = [] # names是区域名称（中文）
    databases = [] # databases是url相关信息
    for area in areas:
        str = area.get('href').split('/')
        databases.append(str[5])
        names.append(area.text)
    return names,databases

def download(year): # 爬取城市的总平均信息
    headers = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

    url = 'https://www.anjuke.com/fangjia/' + city + str(year)

    req = requests.get(url=url, headers=headers[random.randint(0,2)])
    req.encoding = req.apparent_encoding
    html = req.text
    req.close()

    bf = BeautifulSoup(html, 'html.parser')

    div_own = bf.find('div', class_='fjlist-box boxstyle2')
    dates = div_own.find_all('b')
    prices = div_own.find_all('span')
    trendency = div_own.find_all('em')

    # 操作数据库
    client = pymongo.MongoClient('localhost', 27017)
    db = client["HousePriceHistory"] # 连接数据库
    #collist = db.list_collection_names() # 获取当前数据库下的所有集合名字
    col = db[city] # 操作相应的集合
    #if "suzhou" in collist: #若存在该collection，先清空
        #db.drop_collection(col)
    for i in range(len(dates)): #插入数据
        dict_final = {"city_name": city_name, "area": "1", "year": dates[i].text[0:4], "month": dates[i].text[5:7],
                      "price": prices[i].text, "trendency": trendency[i].text}
        col.insert_one(dict_final)

def download_areas(year,area,name):  # 爬取城市各个区域的信息
    headers = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

    url = 'https://www.anjuke.com/fangjia/'+ city + str(year) +  '/' + area
    req = requests.get(url=url, headers=headers[random.randint(0,2)])
    req.encoding = req.apparent_encoding
    html = req.text
    req.close()
    bf = BeautifulSoup(html, 'html.parser')
    div_own = bf.find('div', class_='fjlist-box boxstyle2')

    dates = div_own.find_all('b')
    prices = div_own.find_all('span')
    trendency = div_own.find_all('em')

    client = pymongo.MongoClient('localhost', 27017)
    db = client["HousePriceHistory"] # 连接数据库
    col = db[city] # 操作相应的集合

    for i in range(len(dates)): #插入数据
        dict_final = {"city_name": city_name, "area": name, "year": dates[i].text[0:4], "month": dates[i].text[5:7],
                      "price": prices[i].text, "trendency": trendency[i].text}
        col.insert_one(dict_final)


if __name__ == "__main__":
    client = pymongo.MongoClient('localhost', 27017)
    db = client["HousePriceHistory"]  # 连接数据库
    col = db[city]  # 操作相应的集合
    collist = db.list_collection_names() # 获取当前数据库下的所有集合
    if city in collist: # 若集合已存在，则先清空
        db.drop_collection(col)

    year = 2018
    names, areas = get_area()
    while year!=2012:
        print("......正在下载",city_name,year,"年的房价数据......")
        download(year=year)
        for i in range(len(names)):
            download_areas(year=year,area=areas[i],name=names[i])
        year -= 1
    print("downloaded!")

