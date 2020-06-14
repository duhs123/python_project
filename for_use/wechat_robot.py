# coding: utf-8
import itchat
import requests
from itchat.content import *

key = '7f738b5049f94e2585cedd93a02ed606'


def tuling(info):
    url = "http://www.tuling123.com/openapi/api?key=%s&info=%s" % (key, info)
    r = requests.get(url)
    return r.json().get('text')


@itchat.msg_register(TEXT)
def text_reply(msg):
    # if msg.User['NickName'] == '小都':
    #     pass
    # else:
    #     return_text = tuling(msg.text)
    #     # msg.user.send(return_text)
    return tuling(msg.text)


@itchat.msg_register(
    [PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    # print msg['Type']
    # print msg['FileName']
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])


@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
    group_list = list()
    # 针对指定群回复
    group_list.append(u'自己群聊')
    # 当然如果只想针对@你的人才回复，可以设置if msg['isAt']:
    if msg.User['NickName'] in group_list and msg['isAt']:
        return tuling(msg.text)
    else:
        pass


itchat.auto_login(hotReload=True)
itchat.run()