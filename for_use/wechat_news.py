#coding = utf-8
import itchat
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
    weather_info = weather[0]
    # weather_info = '{}\n更新时间：{}'.format(weather[0],up_time[0])
    # print(weather[0])
    # print('更新时间：',up_time[0])
    ask_ok = 'n'
    if ask_ok == 'Y' or ask_ok == 'y':
        pat_more_weather = re.compile('<li class="li. hot".*?\n<i></i>.<span>(.*?)</span>\n<em>(.*?)</em>\n<p>(.*?)</p>.*?\n</li>',re.S)
        more_weather = pat_more_weather.findall(content)
        for item in more_weather:
            if item[1] != '减肥指数':
                # print(item[1],':',item[0],',',item[2])
                weather_info = '{}\n{}：{}，{}'.format(weather_info,item[1],item[0],item[2])
            else:
                # print(item[1],':',item[2])
                weather_info = '{}\n{}：{}'.format(weather_info, item[1], item[2])
    return weather_info
# 爬取不同城市天气
def spaw_weather(cities):
    cityCodeDict = createCityCode()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7'
    }
    weathers = []
    for city in cities:
        cityCode = cityCodeDict[city]  # 得到城市代码
        url = 'http://www.weather.com.cn/weather1d/%d.shtml' % cityCode  # 得到城市天气网址
        weathers.append('{}\n{}'.format(city,spider(url, headers)))
    return weathers
# 发送微信信息
def wechat_send(infos):
    itchat.auto_login(hotReload=True)
    for info in infos:
        itchat.send(info, toUserName=itchat.search_chatrooms(name=u'自己群聊')[0]['UserName'])
    itchat.dump_login_status()

if __name__ == '__main__':
    cities = ['菏泽','哈密','上海']
    weathers = spaw_weather(cities)
    wechat_send(weathers)
