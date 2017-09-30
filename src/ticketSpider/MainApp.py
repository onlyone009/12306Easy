##!/usr/bin/env python
## -*- coding: utf-8 -*-
#'''
#Created on 2017-9-9
#
#@author: Administrator
#'''
#import urllib
#import os.path
#import json
#import ssl
#ssl._create_default_https_context = ssl._create_unverified_context()
#filename = 'cookie.txt'
#def queryTickets():
#     
#        headers = {'User-Agent' :'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
#                   'Referer':'https://kyfw.12306.cn/otn/leftTicket/init'}
#        data = {
#                'leftTicketDTO.train_date':'2017-09-21',
#                'leftTicketDTO.from_station':'SZQ',
#                'leftTicketDTO.to_station':'GZQ',
#                'purpose_codes':'ADULT'
#                }
#        if(os.path.exists(filename)): #保存cookice 中的tt_webid ，否则每次请求新闻都是一个样子
#            cookie = cookielib.MozillaCookieJar()
#            cookie.load(filename, ignore_discard=True, ignore_expires=True)
#        else :
#            cookie = cookielib.MozillaCookieJar(filename)
#        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
#        request = urllib2.Request('https://kyfw.12306.cn/otn/leftTicket/queryX?'+urllib.urlencode(data),headers=headers,unverifiable=False)
#        response =  opener.open(request)
#        if(os.path.exists(filename) == False):
#            cookie.save(ignore_discard=True, ignore_expires=True)
##        d =json.load(response)
#        print "queryTickets   ",response.read()
#if __name__ == '__main__':
#    queryTickets()
