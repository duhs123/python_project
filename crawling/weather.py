#coding: utf-8
import pandas as pd
import requests
import re

#创建一个字典存储中国天气网城市代码
def createCityCode():
    fh = r'中国天气网城市代码.csv'
    data = pd.read_csv(fh,engine='python',encoding='utf-8')
    data = data.dropna()
    # print(data)
    cityCodeDict = {}
    for name,code in zip(data[r'城市名称'],data[r'城市代码']):
        cityCodeDict[name] = code
    return cityCodeDict

#天气爬虫
def spider(url,headers):
    response = requests.get(url,headers)
    content = response.content.decode('utf-8')
    pat_weather = re.compile('<input type="hidden" id="hidden_title" value="(.*?)" />')
    pat_up_time = re.compile('<input type="hidden" id="fc_24h_internal_update_time" value="(.*?)"/>')
    weather = pat_weather.findall(content)
    up_time = pat_up_time.findall(content)
    print(weather[0])
    print('更新时间：',up_time[0])
    # ask_ok = input('是否深入查看（Y/N）：')
    ask_ok = 'y'
    if ask_ok == 'Y' or ask_ok == 'y':
        pat_more_weather = re.compile('<li class="li. hot".*?\n<i></i>.<span>(.*?)</span>\n<em>(.*?)</em>\n<p>(.*?)</p>.*?\n</li>',re.S)
        more_weather = pat_more_weather.findall(content)
        for item in more_weather:
            if item[1] != '减肥指数':
                print(item[1],':',item[0],',',item[2])
            else:
                print(item[1],':',item[2])


def main():
    cityCodeDict = createCityCode()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7'
    }
    while (True):
        try:
            cityName = input('请输入城市名称(按q/Q键退出)：')
            if cityName == 'q' or cityName == 'Q':
                break
            cityCode = cityCodeDict[cityName]  #得到城市代码
            url = 'http://www.weather.com.cn/weather1d/%d.shtml' % cityCode  #得到城市天气网址
            # print(url)
            spider(url,headers)
        except:
            print('未查到%s城市，请重新输入：'%cityName)
if __name__ == '__main__':
    main()

