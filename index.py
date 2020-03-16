#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import web
import time
import threading
import urllib2
import hashlib
import RPi.GPIO as GPIO
import signal  
import atexit
import send
import pygame
from PIL import Image
from array import *
from lxml import etree
from weixin import WeiXinClient
from weixin import APIError
from weixin import AccessTokenError



#传感器位置
#LIGHTPORT = 11 #继电器pin11 GPIO17 

#MOTORPORT = [,,,] #步进电机IN1,IN2,IN3,IN4
flag=0 # close door =0
open_door_flag=0# open door flag ,press open , =1
times=0
data=0
a=0


 
urls = (
'/wx','WeixinInterface'
)


my_appid = 'wxecb727e7e5aede73' #填写你的appid
my_secret = 'a85dfba90937ffb57d20a783888b55f9' #填写你的app secret
 
def _check_hash(data):
    signature=data.signature
    timestamp=data.timestamp
    nonce=data.nonce
    #自己的token
    token="hello" #这里改写你在微信公众平台里输入的token
    #字典序排序
    list=[token,timestamp,nonce]
    list.sort()
    sha1=hashlib.sha1()
    map(sha1.update,list)
    hashcode=sha1.hexdigest()
    #sha1加密算法        
 
    #如果是来自微信的请求，则回复echostr
    if hashcode == signature:
        return True
    return False
 

def _do_event_subscribe(server, fromUser, toUser, xml):
    return server._reply_text(fromUser, toUser, u'欢迎关注此微信号，具体功能请点击下方菜单')
    
def _do_event_unsubscribe(server, fromUser, toUser, xml):
    return server._reply_text(fromUser, toUser, u'bye!')

def _do_event_SCAN(server, fromUser, toUser, xml):
    pass

def _do_event_LOCATION(server, fromUser, toUser, xml):
    pass

def _do_event_CLICK(server, fromUser, toUser, xml):
    key = xml.find('EventKey').text
    try:
        return _weixin_click_table[key](server, fromUser, toUser, xml)
    except KeyError, e:
        print '_do_event_CLICK: %s' %e
        return server._reply_text(fromUser, toUser, u'Unknow click: '+key)

_weixin_event_table = {
    'subscribe'     :   _do_event_subscribe,
    'unsbscribe'    :   _do_event_unsubscribe,
    'SCAN'          :   _do_event_SCAN,
    'LOCATION'      :   _do_event_LOCATION,
    'CLICK'         :   _do_event_CLICK,
}


def _do_click_SNAPSHOT(server, fromUser, toUser, xml):
    data = None
    print server.client.access_token
    
    print '1'
    print server.client.access_token
    err_msg = 'snapshot fail: '
    try:
        data = _take_snapshot('127.0.0.1', 8080, server.client)
    except Exception, e:
        err_msg += str(e)
        print '_do_click_SNAPSHOT', err_msg
        return server._reply_text(fromUser, toUser, err_msg)
    return server._reply_image(fromUser, toUser, data.media_id)

def _take_snapshot(addr, port, client):
    url = 'http://%s:%d/?action=snapshot' %(addr, port)
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req, timeout = 2)
    return client.media.upload.file(type='image', pic=resp)


def _do_DOOR_ON(server, fromUser, toUser, xml):
        global open_door_flag
        global flag
        global data
        data=_call_110(server.client)
	print 'hello2'
	if flag==0:
            open_door_flag=1
            
            return server._reply_text(fromUser, toUser, u'''enter passwd ''')	
        else:
            return server._reply_text(fromUser, toUser, u'''already open ''')	

def _do_DOOR_OFF(server, fromUser, toUser, xml):
        global flag
        if flag ==1:
            flag =0 # do motor close
            atexit.register(GPIO.cleanup)    
            servopin = 21  
            GPIO.setmode(GPIO.BCM)  
            GPIO.setup(servopin, GPIO.OUT, initial=False)  
            p = GPIO.PWM(servopin,50) #50HZ  
            p.start(0)  
            for i in range(1,7):           #开
		p.ChangeDutyCycle(12.5) #设置转动角度  
		time.sleep(0.02)                      #等该20ms周期结束  
		p.ChangeDutyCycle(0)                  #归零信号
            return server._reply_text(fromUser, toUser, u'''close door ''')
        else:
            return server._reply_text(fromUser, toUser, u'''already close''')
    
def _call_110(client):
        
        return client.media.upload.file(type='image', png=open('/home/pi/1.jpg', 'rb'))
	
def _qrcode_init(client):
	return client.media.upload.file(type='image', png=open('/home/pi/1.jpg', 'rb'))

def _do_GUEST_RE(server, fromUser, toUser, xml):
        send.sendmsg('oFfru09XqsVOPTHRBXooncms-xBc','have guest request,click snapshop chaeck identity ')
        return server._reply_text(fromUser, toUser, u''' wait for respond for a second''')	

# 最后看看都有哪些用户
	

        data = _call_110(server.client)
        return server._reply_image(fromUser, toUser, data.media_id)
            
    
def _do_click_V1001_HELP(server, fromUser, toUser, xml):
    data = _call_110(server.client)
    #return server._reply_image(fromUser, toUser, data.media_id)
    send.sendmsg(fromUser,'http://kakalt.vipgz1.idcfengye.com/?action=stream ')
    return server._reply_text(fromUser, toUser, u'''此微信公众平台基于树莓派，可以随时随地的以微信端为控制器，与终端进行交互。具体功能请点击菜单选项 ''')


    
_weixin_click_table = {
    
    'V1001_SNAPSHOT'        :   _do_click_SNAPSHOT,
	'V1001_DOOR_ON'         :   _do_DOOR_ON,
	#'V1001_DOOR_OFF'		:	_do_DOOR_OFF,
	'V1001_DOOR_OFF'        :   _do_DOOR_OFF,
	'V1001_GUEST_RE'		:	_do_GUEST_RE,
    'V1001_HELP'            :   _do_click_V1001_HELP
	
}





   
class WeixinInterface:
 
    def __init__(self):
      
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
        self.client = WeiXinClient(my_appid, my_secret, fc=True, path='/tmp')
        a=self.client.request_access_token()
       
      
        
 
    def _recv_text(self, fromUser, toUser, xml):
        global open_door_flag
        global flag
        global times
        global data
        content = xml.find('Content').text
        reply_msg = content
	if open_door_flag==1:
            if reply_msg=='123' :
                flag=1 #open door ,motor open 
                open_door_flag=0
                atexit.register(GPIO.cleanup)    
                servopin = 21  
                GPIO.setmode(GPIO.BCM)  
                GPIO.setup(servopin, GPIO.OUT, initial=False)  
                p = GPIO.PWM(servopin,50) #50HZ  
                p.start(0)  
                for i in range(1,7):
                    p.ChangeDutyCycle(2.5) #设置转动角度  
                    time.sleep(0.02)                      #等该20ms周期结束  
                    p.ChangeDutyCycle(0)                  #归零信号
                return self._reply_text(fromUser, toUser, u'success' )
            else:
                times=times+1
                print times
                if times<=3:
                    return self._reply_text(fromUser, toUser, u'error')
                else:
                    open_door_flag=0
                    times =0
                    return self._reply_image(fromUser, toUser, data.media_id)
                    
        else:
            return self._reply_text(fromUser, toUser, u'我还不能理解你说的话:' + reply_msg)
        

    def _recv_event(self, fromUser, toUser, xml):
        event = xml.find('Event').text
        try:
            return _weixin_event_table[event](self, fromUser, toUser, xml)
        except KeyError, e:
            print '_recv_event: %s' %e
            return server._reply_text(fromUser, toUser, u'Unknow event: '+event)

    def _recv_image(self, fromUser, toUser, xml):
		return self.render.reply_text(fromUser,toUser,int(time.time()),u"接收图片处理的功能正在开发中")

    def _recv_voice(self, fromUser, toUser, xml):
        return self.render.reply_text(fromUser,toUser,int(time.time()),u"接收声音处理的功能正在开发中")

    def _recv_video(self, fromUser, toUser, xml):
        return self.render.reply_text(fromUser,toUser,int(time.time()),u"接收视频处理的功能正在开发中")

    def _recv_location(self, fromUser, toUser, xml):
        return self.render.reply_text(fromUser,toUser,int(time.time()),u"接收位置处理的功能正在开发中")

    def _recv_link(self, fromUser, toUser, xml):
        return self.render.reply_text(fromUser,toUser,int(time.time()),u"接收链接处理的功能正在开发中")

    def _reply_text(self, toUser, fromUser, msg):
        return self.render.reply_text(toUser, fromUser, int(time.time()),msg)

    def _reply_image(self, toUser, fromUser, media_id):
        return self.render.reply_image(toUser, fromUser, int(time.time()), media_id)

    def _reply_news(self, toUser, fromUser, title, descrip, picUrl, hqUrl):
        return self.render.reply_news(toUser, fromUser, int(time.time()), title, descrip, picUrl, hqUrl)


    def GET(self):
        #获取输入参数
	data = web.input()
        if _check_hash(data):
            return data.echostr

        
    def POST(self):        
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        
        if msgType == 'text':
            return self._recv_text(fromUser, toUser, xml)
	    
        if msgType == 'event':
            return self._recv_event(fromUser, toUser, xml)
	    
        if msgType == 'image':
            return self._recv_image(fromUser, toUser, xml)
	   
        if msgType == 'voice':
            return self._recv_voice(fromUser, toUser, xml)
	    
        if msgType == 'video':
            return self._recv_video(fromUser, toUser, xml)
	    
        if msgType == 'location':
            return self._recv_location(fromUser, toUser, xml)
	    
        if msgType == 'link':
            return self._recv_link(fromUser, toUser, xml)
	    
        else:
            return self._reply_text(fromUser, toUser, u'Unknow msg:' + msgType)


application = web.application(urls, globals())

if __name__ == "__main__":
    application.run()
