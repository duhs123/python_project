import itchat

# itchat.auto_login()
itchat.auto_login(hotReload=True)
itchat.send('Hello, filehelper', toUserName='filehelper')
itchat.dump_login_status()