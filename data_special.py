# -*_ coding:UTF-8 -*_
import requests
from bs4 import BeautifulSoup
import random
import pymongo

# 每次更换url 即可爬取一个省份的所有历史房价数据
url = 'https://www.anjuke.com/fangjia/neimenggu2019/'
province = "NeiMengGu_"
city = "huhehaote"
city_name = "呼和浩特"
province_name = "内蒙古"
year_ = "2018"


def get_area(city,year): # 获取城市所属区的相关信息：网址url+区域名称
    headers = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

    url = 'https://www.anjuke.com/fangjia/'+city+year
    req = requests.get(url=url, headers=headers[random.randint(0,2)],timeout=(3,7))
    req.encoding = req.apparent_encoding
    html = req.text
    req.close()
    bf = BeautifulSoup(html, 'html.parser')
    div = bf.find('div',class_='items')
    areas = div.find_all('a')
    names = [] # names是区域名称（中文）
    databases = [] # databases是url相关信息
    for area in areas:
        str = area.get('href').split('/')  # 从<a href="http://www.anjuke.com/fangjia/nanjing2019/jiangninga/">江宁</a>字段中选择
        databases.append(str[5]) # https://www.anjuke.com/fangjia/nanjing2019/jiangninga/选自jiangninga字段
        names.append(area.text) #  从<a href="http://www.anjuke.com/fangjia/nanjing2019/jiangninga/">江宁</a>字段中选择江宁字段
    return names,databases

def download(city,city_name,year): # 爬取城市的总平均信息
    headers = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
    url = 'https://www.anjuke.com/fangjia/' + city + str(year)
    req = requests.get(url=url, headers=headers[random.randint(0,2)],timeout=(3,7))
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
    global province,province_name # 用全局变量
    col = db[province+city] # 操作相应的集合
    for i in range(len(dates)): #插入数据
        dict_final = {"city_name": city_name, "area": "1", "year": dates[i].text[0:4], "month": dates[i].text[5:7],
                      "price": prices[i].text, "trendency": trendency[i].text,"province":province_name}
        col.insert_one(dict_final)

def download_areas(city,city_name,year,area,name):  # 爬取城市各个区域的信息
    headers = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

    url = 'https://www.anjuke.com/fangjia/'+ city + str(year) +  '/' + area
    req = requests.get(url=url, headers=headers[random.randint(0,2)],timeout=(3,7))
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
    global province,province_name
    col = db[province+city] # 操作相应的集合

    for i in range(len(dates)): #插入数据
        dict_final = {"city_name": city_name, "area": name, "year": dates[i].text[0:4], "month": dates[i].text[5:7],
                      "price": prices[i].text, "trendency": trendency[i].text,"province":province_name}
        col.insert_one(dict_final)


if __name__ == "__main__":

    client = pymongo.MongoClient('localhost', 27017)
    db = client["HousePriceHistory"]  # 连接数据库
    col = db[province+city]  # 操作相应的集合
    collist = db.list_collection_names() # 获取当前数据库下的所有集合
    if  province+city in collist: # 若集合已存在，则先清空
        db.drop_collection(col)
    year = 2019 # 爬取的初始年份
    names, areas = get_area(city, year_)
    while year!=2012: # 爬到2013年为止
        print("......正在下载",city_name,year,"年的房价数据......")
        download(city=city,city_name=city_name,year=year) #爬取比如南京的房价信息
        for i in range(len(names)):
            # 爬取南京所属所有区的房价信息
            download_areas(city=city,city_name=city_name,year=year,area=areas[i],name=names[i])
        year -= 1
    print("下载成功！")

