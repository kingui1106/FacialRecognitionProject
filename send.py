#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pip3 install requests
import requests
import json
import urllib
import os
import web
from weixin import WeiXinClient
from weixin import APIError
from weixin import AccessTokenError



my_appid = 'wxecb727e7e5aede73' #填写你的appid
my_secret = 'a85dfba90937ffb57d20a783888b55f9' #填写你的app secret


class WeixinInterface:
 
    def __init__(self):
      
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
        self.client = WeiXinClient(my_appid, my_secret, fc=True, path='/tmp')
        a=self.client.request_access_token()

def get_access_token():
	#url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'
	#data={'appid':'wxecb727e7e5aede73',
	#	  'secret':'a85dfba90937ffb57d20a783888b55f9'}

	#data=urllib.urlencode(data)
	#html=urllib.urlopen(url,data)

	#result=json.load(html)
	server = WeixinInterface()
        server.__init__()
	access_token=server.client.access_token
	print access_token
	print 'send'
	return access_token
	#access_token=result["access_token"]
	#print access_token
	#return access_token


def sendmsg(openid,msg):

    access_token = get_access_token()

    body = {
        "touser": openid,
        "msgtype": "text",
        "text": {
            "content": msg
        }
    }
    response = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
        params={
            'access_token': access_token
        },
        data=json.dumps(body, ensure_ascii=False)
    )
    # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
    result = response.json()
    print(result)

def test():
    pass


if __name__ == '__main__':
    test()
    
    
