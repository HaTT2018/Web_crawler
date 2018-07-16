# -*- coding: utf-8 -*-
import urllib
import random
from bs4 import BeautifulSoup
import csv
import time

start = time.time()#to get the start time
#some agents (but maybe not necessary)
Agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'AppleWebKit/537.36 (KHTML, like Gecko)', 'Chrome/66.0.3359.181 Safari/537.36']
#choose an agent randomly
User_Agent = random.choice(Agents)
#the root url which contains the price of houses in Hangzhou 
url = 'https://hz.lianjia.com/ershoufang/pg'
#the request header
Header = {
            'User_Agent':User_Agent,
            'Host': 'hm.baidu.com',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive'
        }

#it is a function that can generate a soup of a webpage
#I used urllib to get the response
#if the status is not 200, we will print the status and the program will stop
def get_html_soup(url,page):
    global Header
    url = url+str(page)
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    status = response.code
    try:
        soup = BeautifulSoup(response,'lxml')
        return soup
    except:
        print(status)

#to get the unit price of a house (how much for each m2)
def get_house_unit_price(soup):
    unit_price_list = [i.get('data-price') for i in soup.find_all('div',class_='unitPrice')]
    return unit_price_list

#to get the total price of a house (how much for each m2)
def get_house_total_price(soup):
    total_price_list = [i.find('span').string for i in soup.find_all('div',class_='totalPrice')]
    return total_price_list
#the area of a house probably can be caculated by total price/unit price
'''
def get_house_area(soup):
    house_area_list = [i.a.string for i in soup.find_all('div',class_='houseInfo')]
    return house_area_list
'''
#get the name of the house 
def get_house_name(soup):
    house_name_list = [i.a.string for i in soup.find_all('div',class_='houseInfo')]
    return house_name_list

#get more info of the house 
def get_house_type(soup):
    house_type_list = [i.string for i in soup.find_all('div',class_='houseInfo')]
    return house_type_list

def write_into_csv(url,path,pages):
    with open(path,'a',encoding='utf-8',newline='') as file:
        titles = ['单价', '总价','面积','楼盘','户型/详细信息']
        writer = csv.writer(file)
        writer.writerow(titles)
        for page in range(pages):
            soup = get_html_soup(url,page)

            unit_price_list = get_house_unit_price(soup)
            total_price_list = get_house_total_price(soup)
            area_list = [float(total_price_list[i])/float(unit_price_list[i]) for i in range(len(unit_price_list))]
            name_list = get_house_name(soup)
            type_list = get_house_type(soup)

            data = [[unit_price_list[i], total_price_list[i], area_list[i],name_list[i], type_list[i]] for i in range(len(unit_price_list))]
            writer.writerows(data)
            print('successfullly downloaded page number %i'%(page+1))
        file.close()



def main():
    global url
    page = 99
    write_into_csv(url,r'C:\\Users\\10169\\Desktop\\house_price_hz.csv',page)

main()

end = time.time()
print(end-start)