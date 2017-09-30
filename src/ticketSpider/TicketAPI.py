#!/usr/bin/env python
# -*- coding: utf-8 -*-
#response = urllib2.urlopen("https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date=2017-09-21&leftTicketDTO.from_station=SZQ&leftTicketDTO.to_station=GZQ&purpose_codes=ADULT")
import re
import random
import urllib
import json
from ticketSpider.Model import PassengersModel
from PIL import Image
from xmlrpclib import datetime
import time
from pip._vendor import requests
#余票查询URL
query_url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?'
init_url='https://kyfw.12306.cn/otn/leftTicket/log?'
#图片验证码 校验URL
check_pic_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
#获取图片验证码 
captcha_check_pic_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
#账号校验URL
login_url = 'https://kyfw.12306.cn/passport/web/login'
#tk码获取URL
get_uamtk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
#程序获取授权URL
auth_clinet_url = 'https://kyfw.12306.cn/otn/uamauthclient'
#获取已添加乘客信息
get_passengres_added_url ='https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
#订单提交请求第一步 
submit_order_request_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
#订单提交第二步 检查订单信息
check_order_url ='https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
#订单提交第三步 查询订单队列
get_queen_count_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
#提交订单到队列WC
confirmGoForQueue_url = "https://kyfw.12306.cn/otn/confirmPassenger/confirmGoForQueue"
#提交订单到队列dc
confirmSingleForQueue_url = "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
#查询订单ID
queryOrderWaitTime_url='https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime'
#正式提交订单wd
resultOrderForWcQueue_url ='https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForWcQueue'
#正式提交订单sc
resultOrderForDcQueue_url = 'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue'
#查询未完成订单
queryMyOrderNoComplete_url ='https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete'
#查询已完成订单
queryMyOrder_url = 'https://kyfw.12306.cn/otn/queryOrder/queryMyOrder'
init_WC_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initWc'
init_Dc_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
stations ={} 
stations_cn = {}
seatType=['商务座','特等座','一等座','二等座','硬座','无座','软卧','动卧',"硬卧",'软座','高级软卧']
#调用接口的时候座位类型需要抓换为固定的ID
seatTypeMap = {"特等座":"P","一等座":"M","二等座":"O","硬座":1,"软卧":4,"动卧":"F","硬卧":3,"商务座":9}
secretMap = {"%2B":"+","%2F":"/","%0A":"\n","%3D":"="}
HEADERS = {'User-Agent' :'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                   'Referer':'https://kyfw.12306.cn/otn/leftTicket/init'}
#P 特等座 ，0 二等座， M 一等， 3 硬卧 ，4软卧，F 动卧, 1硬座/无座 ， 7->一等软座 8->二等软座 9商务座 B->混编硬座
mySession = requests.session() #全局Session 用来登录购票下订单一系列活动
isLogin = False
globalRepeatSubmitToken = ""
key_check_isChange = ""
mySession.headers = {
            'Accept-Language': 'zh-CN',
            'User-Agent' :'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Referer':'https://kyfw.12306.cn/otn/leftTicket/init',
            'Host': 'kyfw.12306.cn',
            'Connection': 'Keep-Alive'
        }
#通过点击位置获取验证码坐标
def getLocationByPos(pos):
    post = []
    offsetsX = 0  # 选择的答案的left值,通过浏览器点击8个小图的中点得到的,这样基本没问题
    offsetsY = 0  # 选择的答案的top值
    for ofset in pos:
        if ofset == 0:
            offsetsX = 35
            offsetsY = 46
        elif ofset == 1:
            offsetsX = 112
            offsetsY = 43
        elif ofset == 2:
            offsetsX = 180
            offsetsY = 45
        elif ofset == 3:
            offsetsX = 252
            offsetsY = 43
        elif ofset == 4:
            offsetsX = 37
            offsetsY = 114
        elif ofset == 5:
            offsetsX = 107
            offsetsY = 114
        elif ofset == 6:
            offsetsX = 182
            offsetsY = 115
        elif ofset == 7:
            offsetsX = 252
            offsetsY = 120
        else:
            pass
        post.append(offsetsX)
        post.append(offsetsY)
    return post
#查询火车票        
def getTrainNoList(back_date,train_date,from_station,to_station):  
    HEADERS = {'User-Agent' :'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                   'Referer':'https://kyfw.12306.cn/otn/leftTicket/init'}
    post_data= {'back_train_date':back_date,  
                '_json_att':"",'flag':'dc',  
                'leftTicketDTO.from_station':from_station,  
                'leftTicketDTO.to_station':to_station,  
                'leftTicketDTO.train_date':train_date,  
                'pre_step_flag':'index'
    }  
  
    init_resp=requests.post(init_url,data=post_data,headers=HEADERS,allow_redirects=True,verify=False)  
    cookies=init_resp.cookies  
#    print (cookies)
    cookies.set('_jc_save_fromStation', from_station, domain='kyfw.12306.cn', path='/')  
    cookies.set('_jc_save_toStation', to_station, domain='kyfw.12306.cn', path='/')  
    cookies.set('_jc_save_fromDate', train_date, domain='kyfw.12306.cn', path='/')  
    cookies.set('_jc_save_toDate', back_date, domain='kyfw.12306.cn', path='/')  
    cookies.set('_jc_save_wfdc_flag', 'dc', domain='kyfw.12306.cn', path='/')  
    cookies.set('fp_ver', '4.5.1', domain='kyfw.12306.cn', path='/')  
    cookies.set('RAIL_DEVICEID', 'q8rT7ImgRQKKqSggROZ0zFV9OUJjgkg4_-PTk3pEXX86oDDYuCQoj2jP4k8D_ZkAvsrIyx_lfu-BskU4c_w9zjTrZ1Az3GpHbOV5BYdjE3DfNLcnop0JdGUXxxyASXA32FTQ4j8TuNB1JCCbMRWf-fP5a8QNNwKf', domain='kyfw.12306.cn', path='/')  
#    print (cookies)
#    mySession.cookies.set('RAIL_DEVICEID', 'q8rT7ImgRQKKqSggROZ0zFV9OUJjgkg4_-PTk3pEXX86oDDYuCQoj2jP4k8D_ZkAvsrIyx_lfu-BskU4c_w9zjTrZ1Az3GpHbOV5BYdjE3DfNLcnop0JdGUXxxyASXA32FTQ4j8TuNB1JCCbMRWf-fP5a8QNNwKf', domain='kyfw.12306.cn', path='/')  
    url=query_url+"leftTicketDTO.train_date="+train_date+"&leftTicketDTO.from_station="+from_station+"&leftTicketDTO.to_station="+to_station+"&purpose_codes=ADULT"  
#    try:  
    response = requests.get(url, headers=HEADERS, allow_redirects=True,cookies=cookies,verify=False,timeout=10)  
#    data=""  
#    print  (response.text)
    return (response.text)
#    try:
#        res = response.json()
#        if(res.get('httpstatus') == 200):
#            data = res.get('data')
#            result = data.get('result')
#            for d in result:
#                print (d)
#    except:
#        print ('没有查询到车辆信息')
#获取城市信息列表
def queryCityMap():
#    cook = requests.get('https://kyfw.12306.cn/otn/leftTicket/init',verify=False );
#    print (cook.cookies)
#    print(cook.cookies['RAIL_DEVICEID'])
    global stations
    global stations_cn
    if len(stations) == 0:
        init_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9025'
        text = requests.get(init_url,verify=False)  
        stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', text.text)
        stations = dict(stations)
        stations_cn = stations
        stations = dict(zip(stations.values(), stations.keys()))#key value翻转
        if len(stations) and  len(stations_cn):
            print 'queryCityMap 初始化加载城市列表成功'
        else:
            print 'queryCityMap 加载城市列表失败'
    return stations, stations_cn

def getCheciImg():
    HEADERS = {'User-Agent' :'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                   'Referer':'https://kyfw.12306.cn/otn/leftTicket/init'}
    global mySession
    response =mySession.get(url=(check_pic_url+'&'+ str(random.random())),headers=HEADERS,verify=False)  
    raw = response.content
    with open("./tmp.jpg", 'wb') as fp:
        fp.write(raw)
    return Image.open("./tmp.jpg")  

#校验 验证码
def verifyCheckCode(answer):
#  创建一个网络请求session实现登录验证  
    data = {  
            'login_site':'E',           #固定的  
            'rand':'sjrand',            #固定的  
            'answer':answer    #验证码对应的坐标，两个为一组，跟选择顺序有关,有几个正确的，输入几个  
        }  
        # 发送验证
    global mySession
    cont = mySession.post(url=captcha_check_pic_url,data=data,headers=HEADERS,verify=False)  
    dic = json.loads(cont.content)  
    print dic
    if dic['result_code'] == '4':
        return True
    return False

#登陆
def loginTo(userName,pwd):  
        data = {  
            'username':userName,  
            'password':pwd,  
            'appid':'otn'  
        }
        global mySession
        #1 验证图片验证码最后， 验证账号密码
        result = mySession.post(url=login_url,data=data,headers=HEADERS,verify=False)  
        dic = json.loads(result.content)  
        print result.content  
        mes = dic['result_message']  
        print dic
        # 结果的编码方式是Unicode编码，所以对比的时候字符串前面加u,或者mes.encode('utf-8') == '登录成功'进行判断，否则报错  
        if mes == u'登录成功':  
            data = {  
            'appid':'otn',
            '_json_att':None
            }  
            #2  验证账号密码 成功之后， 获取newapptk码
            result2 = mySession.post(url=get_uamtk_url,data=data,headers=HEADERS,verify=False)  
            dic = json.loads(result2.content)
            tk = dic['newapptk']
            data = {  
            'tk':tk,
            '_json_att':None
            }
            #3   获取tk码 之后，进行收授权，获得到角色名称
            result3= mySession.post(url=auth_clinet_url,data=data,headers=HEADERS,verify=False)  
            dic_3 = json.loads(result3.content)  
            mes = dic_3['result_message']
            if  mes == u'验证通过':
                isLogin = True
                print "账号密码验证成功"
                return  getPassengerDTOs()
        else:  
            isLogin = False
            print "账号密码验证失败"
            return None
#查询已添加的乘客信息        
def getPassengerDTOs():
    global mySession
    curHeads = {'User-Agent' :'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                   'Referer':init_WC_url}
    postdata= {
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":globalRepeatSubmitToken
             }
    result = mySession.post(url=get_passengres_added_url,data=postdata,headers=HEADERS,verify=False)  
    mPassengers = []
    dic  = json.loads(result.content)  
    if dic['data']and dic['data']['isExist']:
        normal_passengers =  dic['data']['normal_passengers']
        for  passenge in normal_passengers:
            passenger_name =passenge['passenger_name'] 
            code =int (passenge['code'])
            if passenge.has_key('sex_code'):
                sex_code = passenge['sex_code']
            if passenge.has_key('sex_name'):
                sex_name = passenge['sex_name']
            born_date = passenge['born_date']
            passenger_id_type_code =passenge['passenger_id_type_code']
            passenger_id_type_name =passenge['passenger_id_type_name']
            passenger_id_no = passenge['passenger_id_no']
            passenger_type = passenge['passenger_type']
            passenger_type_name = passenge['passenger_type_name']
            if passenge.has_key('mobile_no'):
                mobile_no = passenge['mobile_no']
            p = PassengersModel(passenger_name,code,sex_code,sex_name,born_date,passenger_id_type_code,
                 passenger_id_type_name,passenger_id_no,passenger_type,passenger_type_name,mobile_no)
#            print p.toArray()
            mPassengers.append(p)
        print '获取联系人成功',
        return  mPassengers
    else:
        print '获取联系人失败',result.content
        
def checkUser():
    global mySession
    postdata = {  
            '_json_att':"",
        }
    result = mySession.post(url="https://kyfw.12306.cn/otn/login/checkUser",data = postdata,headers=HEADERS,verify=False)
    try:
        dic  = json.loads(result.content) 
    except:
        print "checkUser检查失败"
        return False
    if  dic["httpstatus"] == 200 and dic["status"] == True :
        print "checkUser检查成功"
        return True
    else:
        print "checkUser检查失败"
        return False

#获取RepeatSubmitToken
#def getGlobalRepeatSubmitToken():
#    global mySession
#    global  globalRepeatSubmitToken
#    postdata = {  
#            '_json_att':"",
#        }
#    result = mySession.post(url="https://kyfw.12306.cn/otn/confirmPassenger/initDc",data = postdata,headers=HEADERS,verify=False)  
#    match =re.search("var globalRepeatSubmitToken = '(.*?)';", result.content)
#    globalRepeatSubmitToken =match.group(1)
#    print "getGlobalRepeatSubmitToken = {}".format(globalRepeatSubmitToken)  
#    return globalRepeatSubmitToken
      
#订单提交第1 步     订单初始化   
def submitOrderRequest(ticket_secretStr,train_date,back_train_date,purpose_codes,query_from_station_name,query_to_station_name,tour_flag ='dc',):
    checkUser()
    for k,v in secretMap.iteritems(): 
        ticket_secretStr = ticket_secretStr.replace(k, v)
    print ticket_secretStr
    global mySession
    postdata = {  
            'secretStr':ticket_secretStr,
            'train_date':train_date,  
            'back_train_date':back_train_date,  
            'tour_flag':tour_flag,
            'purpose_codes':purpose_codes,
            'query_from_station_name':query_from_station_name,
            'query_to_station_name':query_to_station_name,
            'undefined':"",
        }
    result = mySession.post(url=submit_order_request_url,data= postdata,headers=HEADERS,verify=True)  
    try:
        dic  = json.loads(result.content) 
    except:
        print "订单初始化 失败:{}".format(dic["messages"])
        return False
    if  dic["httpstatus"] == 200 and dic["status"] == True :
        print "订单初始化 成功"
        InitDc()
        return True
    else:
        print "订单初始化 失败:{}".format(dic["messages"])
        return False
#往返
def InitWc():
    global mySession
    global  globalRepeatSubmitToken
    postdata = {  
            '_json_att':"",
        }
    result = mySession.post(url=init_WC_url,data = postdata,headers=HEADERS,verify=False)  
    match =re.search("var globalRepeatSubmitToken = '(.*?)';", result.content)
    globalRepeatSubmitToken =match.group(1)
    print "getGlobalRepeatSubmitToken = {}".format(globalRepeatSubmitToken)  

#单程
def InitDc():
    global mySession
    global  globalRepeatSubmitToken
    global key_check_isChange
    postdata = {  
            '_json_att':"",
        }
    result = mySession.post(url=init_Dc_url,data = postdata,headers=HEADERS,verify=False)  
    s = result.content.find('globalRepeatSubmitToken')  # TODO
    if(s== -1):
        print('找不到 globalRepeatSubmitToken')
    else:
        match =re.search("var globalRepeatSubmitToken = '(.*?)';", result.content)
        globalRepeatSubmitToken =match.group(1)
        print "getGlobalRepeatSubmitToken = {}".format(globalRepeatSubmitToken)   
    k= result.content.find('key_check_isChange')
    
    if(k== -1):
        print('找不到 key_check_isChange')
    else:
        match =re.search("'key_check_isChange':'(.*?)',", result.content)
        key_check_isChange =match.group(1)
        print(' key_check_isChange',key_check_isChange)


#订单提交第2 步 检查订单信息   
def checkOrderInfo(passengerTicketStr,oldPassengerStr):
    global mySession
    for index in passengerTicketStr:
        pass
    postdata= {
        "cancel_flag":2,
        'bed_level_order_num':"000000000000000000000000000000",
        "passengerTicketStr":passengerTicketStr,
       'oldPassengerStr':oldPassengerStr,
        "tour_flag":"dc",
        "randCode":"",
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":globalRepeatSubmitToken
             }
    print postdata
    result = mySession.post(url=check_order_url,data = postdata,headers=HEADERS,verify=False)  
    print result.content
    dic  = json.loads(result.content) 
    if  dic["httpstatus"] == 200 and dic["status"] == True :
        print "订单检查成功"
        return True
    else:
        print "订单检查失败"
        return False
#订单提交第三步 查询排队和余票情况
def getQueueCount(train_date,train_no_Long,train_no,seatType,fromStationTelecode,toStationTelecode,leftTicket,train_location):
    global mySession
    global  globalRepeatSubmitToken
    postdata= {
        "train_date":train_date,
        'train_no':train_no,
        "stationTrainCode":train_no_Long,
       'seatType':seatType,
        "fromStationTelecode":fromStationTelecode,
        "toStationTelecode":toStationTelecode,
        "leftTicket":leftTicket,
        "purpose_codes":"00",
        "train_location":train_location,
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":globalRepeatSubmitToken
             }
    
    print postdata
    result = mySession.post(url=get_queen_count_url,data = postdata,headers=HEADERS,verify=False)  
    print result.content
    dic  = json.loads(result.content) 
    if  dic["httpstatus"] == 200 and dic["status"] == True and dic["data"]:
        ticket  =  dic["data"]["ticket"].split(",")
        haveSeat= 0
        noSeat = 0
        if(len(ticket)>=1):
            haveSeat = ticket[0]
        if(len(ticket)>=2):
            noSeat = ticket[1]
        print "还有余票 {}张,无座{}张".format(haveSeat,noSeat)
        if (haveSeat>0) or (seatType>0):
            return True
        else:
            print "没有可用的票"
            return False  
        return True
    else:
        print "没有可用的票"
        return False  
 
#订单提交第四步，加到订单队列DC
def confirmSingleForQueue(train_location,leftTicketStr,passengerTicketStr="",oldPassengerStr=""):
    global mySession
    global key_check_isChange
    postdata= {
        "passengerTicketStr":passengerTicketStr,
       'oldPassengerStr':oldPassengerStr,
       "purpose_codes":"00",
       "randCode":"",
       "leftTicketStr":leftTicketStr,
       "key_check_isChange":key_check_isChange,
       "train_location":train_location,
       "choose_seats":"",
       "seatDetailType":"000",
        "roomType":"00",
        "dwAll":'N',
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":globalRepeatSubmitToken
             }
    result = mySession.post(url=confirmSingleForQueue_url,data = postdata,headers=HEADERS,verify=False)  
    print result.content
    try:
        dic  = json.loads(result.content) 
    except:
        print "提交单程订单到队列失败"
        return False  
    if  dic["httpstatus"] == 200 and dic["status"] == True and dic['data']['submitStatus']:
        print "提交单程订单到队列成功"
        return True
    else:
        print "提交单程订单到队列失败"
        return False
     
#订单提交第四步，加到订单队列WC
def confirmGoForQueue(train_location,leftTicketStr,passengerTicketStr="",oldPassengerStr=""):
    global mySession
    global key_check_isChange
    postdata= {
        "passengerTicketStr":passengerTicketStr,
       'oldPassengerStr':oldPassengerStr,
       "purpose_codes":"00",
       "randCode":"",
       "leftTicketStr":leftTicketStr,
       "key_check_isChange":key_check_isChange,
       "train_location":train_location,
       "choose_seats":"",
       "seatDetailType":"000",
        "roomType":"00",
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":globalRepeatSubmitToken
             }
    result = mySession.post(url=confirmGoForQueue_url,data = postdata,headers=HEADERS,verify=False)  
    print result.content
    dic  = json.loads(result.content) 
    if  dic["httpstatus"] == 200 and dic["status"] == True :
        print "提交往返订单到队列成功"
        return True
    else:
        print "提交往返订单到队列失败"
        return False
    
def queryOrderWaitTime(tourFlag='dc'):
    print"queryOrderWaitTime"
    global mySession
    postdata= {
        'random': long((time.time() * 100)),
        "_json_att":"",
        "tourFlag":tourFlag,
        "REPEAT_SUBMIT_TOKEN":globalRepeatSubmitToken
             }
    result = mySession.get(url=queryOrderWaitTime_url,data = postdata,headers=HEADERS,verify=False)  
    print result.content
    try:
        dic  = json.loads(result.content) 
    except Exception as e:
        print "订单ID生成失败 :{}".format(e)
        return None
    if  dic["httpstatus"] == 200 and dic["status"] == True  :
        msg = "NA"
        if(dic.has_key("msg")):
            msg = dic["dic"]["msg"]
        if(dic.has_key("errorcode")):
            print "订单ID生成失败：{}".format(msg)
            return None
        else:
            waitCount = dic["dic"]["waitCount"]
            orderId = dic["dic"]["orderId"]
            if(orderId !=""):
                print "订单ID生成成功 {}  msg={}".format(orderId,msg)
                return orderId
            elif waitCount>0:
                return queryOrderWaitTime()
    else:
        print "订单ID生成失败"
        return None

#正式提交订单wc
def resultOrderForWcQueue(orderSequence_no):
    global mySession
    postdata= {
        'orderSequence_no':orderSequence_no,
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":globalRepeatSubmitToken
             }
    result = mySession.post(url=resultOrderForWcQueue_url,data = postdata,headers=HEADERS,verify=False)  
    print result.content
    dic  = json.loads(result.content) 
    if  dic["httpstatus"] == 200 and dic["status"] == True :
        print "正式提交订单成功"
        return True
    else:
        print "正式提交订单失败"
        return False

#正式提交订单dc
def resultOrderForDcQueue(orderSequence_no):
    global mySession
    postdata= {
        'orderSequence_no':orderSequence_no,
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":globalRepeatSubmitToken
             }
    result = mySession.post(url=resultOrderForDcQueue_url,data = postdata,headers=HEADERS,verify=False)  
    print result.content
    try:
        dic  = json.loads(result.content) 
    except:
        print "正式提交订单失败"
        return None
    if  dic["httpstatus"] == 200 and dic["status"] == True :
        print "正式提交订单成功"
        return True
    else:
        print "正式提交订单失败"
        return False
    
#查询未完成订单
def queryMyOrderNoComplete():
    global mySession
    result = mySession.post(url=queryMyOrderNoComplete_url,headers=HEADERS,verify=False)  
    try:
        dic  = json.loads(result.content) 
    except:
        print "未完成订单查询失败"
        return None
    if  dic["httpstatus"] == 200 and dic["status"] == True :
        print "未完成订单查询成功"
        return result.content
    else:
        print "未完成订单查询失败"
        return None
    
#查询已完成订单
def queryMyOrder(queryStartDatem,queryEndDate,pageSize=8,pageIndex = 0,query_where="G"):
    global mySession
    postdata= {
        "queryStartDatem":queryStartDatem,
        'queryEndDate':queryEndDate,
        "come_from_flag":"my_order",
        "pageSize":pageSize,
        "pageIndex":pageIndex,
        "query_where":query_where,
        "sequeue_train_name":""
             }
    result = mySession.post(url=resultOrderForWcQueue_url,data = postdata,headers=HEADERS,verify=False)  
    print result.content
    dic  = json.loads(result.content) 
    if  dic["httpstatus"] == 200 and dic["status"] == True :
        print "已完成订单查询失败"
        return True
    else:
        print "已完成订单查询失败"
        return False   
#queryCityMap()
#result = getTrainNoList('2017-09-22','2017-09-21','GZQ','SYT')

