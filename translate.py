# -*- coding: gb18030
import requests
import json
import csv
import time

youdaourl = 'https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
baiduurl = 'https://fanyi.baidu.com/sug'
headers = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36",
        }

root_path = r'C:\\Users\\10169\\OneDrive - International Campus, Zhejiang University\\Desktop\\TOEFL\\words_day'
def read_words(day):
    global root_path
    global headers
    path = root_path + str(day) + '.txt'
    with open(path,'r') as file:
        words_list = file.readlines()
        file.close()
    return words_list

def translate_use_youdao(word):
    global youdaourl
    data = {
        "i": word,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTIME",
        "typoResult": "false"
        }
    response = requests.post(youdaourl,data=data,headers=headers)
    target = response.json()
    result = target['translateResult'][0][0]['tgt']
    return result

def translate_use_baidu(word):
    global baiduurl
    global headers
    data={
        ' from':'en','to':'zh',
        'query':word, 
        'transtype':'translang',
        'simple_means_flag':'3'
        }
    response = requests.post(baiduurl,data=data,headers=headers)
    result = response.json()['trans'][0]['dst']
    return result

def generate_result_list(words_list,day):
    global root_path
    with open(root_path+str(day)+'translated.csv','a',newline='') as file:
        titles = ['origin','youdao','baidu']
        writer = csv.writer(file)
        writer.writerow(titles)
        for i in range(len(words_list)):
            print('translating No.%i word...'%(i+1))
            try:
                translated_words_youdao = translate_use_youdao(words_list[i])
            except:
                translated_words_youdao = 'FAILED!'
            try:
                translated_words_baidu = translate_use_baidu(words_list[i])
            except:
                translated_words_baidu = 'FAILED!'
            if translated_words_baidu=='FAILED!' and translated_words_youdao=='FAILED!':
                print('FAILING to translate No.%i cell!'%(i+1))
            word_info = [words_list[i],translated_words_youdao,translated_words_baidu]
            writer.writerow(word_info)
        file.close()

def main():
    day=input('day:')
    words_list = read_words(day)
    generate_result_list(words_list,day)

if __name__ == '__main__':
    main()
    a=input('\n\nsuccessfully translated!')
