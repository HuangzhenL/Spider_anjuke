# -*_ coding:UTF-8 -*_
import requests
from bs4 import BeautifulSoup
import random
def get_city_list(): # 获取城市所属区的相关信息：网址url+区域名称
    headers = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

    url = 'https://www.anjuke.com/fangjia/jiangsu2019/'
    req = requests.get(url=url, headers=headers[random.randint(0,2)])
    req.encoding = req.apparent_encoding
    html = req.text
    req.close()
    bf = BeautifulSoup(html, 'html.parser')
    div = bf.find('div',class_='fjlist-box boxstyle1')
    b_tag = div.find_all('b')
    a_tag = div.find_all('a')
    names = [] # names是区域名称（中文）
    databases = [] # databases是url相关信息
    for i in range(len(b_tag)):
        #print(b_tag[i].text)
        a = b_tag[i].text.index('年')
        b = b_tag[i].text.index('房')
        names.append(b_tag[i].text[a+1:b])
        #print(a_tag[i+1])
        str = a_tag[i+1].get('href').split('/')
        c = str[4].index('2')
        databases.append(str[4][:c])
    return names,databases

names,areas = get_city_list()
for i in range(len(names)):
    print(names[i],areas[i])