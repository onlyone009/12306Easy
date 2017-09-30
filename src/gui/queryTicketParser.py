#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017-9-12

@author: Administrator
'''
import json
from ticketSpider.TicketAPI import getTrainNoList, queryCityMap,\
    queryMyOrderNoComplete
import warnings
from sets import Set
from ticketSpider.Model import TicketModel, TicketNoCompletOrder
warnings.filterwarnings("ignore")
tickets = Set()
#def query():
#    tickets = []
#    global_dict ,global_dict_cn= queryCityMap()  
#    r = getTrainNoList('2017-09-22','2017-09-21','GZQ','BJP')
#    res =json.loads(r)
#    if(res.get('httpstatus') == 200):
#        data = res.get('data')
#        result = data.get('result')
#        for d in result:
#            data_list  = d.split('|')
##            for ss in data_list:
##                print(ss)
#                    # 车次号码
#            train_no = data_list[3]
#                # 出发站
#            from_station_code = data_list[6]
#            from_station_name =global_dict[from_station_code]
#                # 终点站
#            to_station_code = data_list[7]
#            to_station_name = global_dict[to_station_code]
#                # 出发时间
#            start_time = data_list[8]
#                # 到达时间
#            arrive_time = data_list[9]
#                # 总耗时
#            time_fucked_up = data_list[10]
#                #商务特等座
#            super_class_seat = data_list[32] or '--'
#                # 一等座
#            first_class_seat = data_list[31] or '--'
#                # 二等座
#            second_class_seat = data_list[30]or '--'
#                #高级 软卧
#            super_soft_sleep = data_list[22]or '--'
#                # 软卧
#            soft_sleep = data_list[23]or '--'
#                # 动卧
#            move_sleep = data_list[24]or '--'
#                # 硬卧
#            hard_sleep = data_list[28]or '--'
#            # 硬座
#            hard_seat = data_list[29]or '--'
#                # 无座
#            no_seat = data_list[26]or '--'
#                #其他
#            other = '--'
#            #备注
#            remind = data_list[1]
##            火车票秘钥
#            secretStr = data_list[0]
##            火车票num
#            train_no_Long = data_list[2]
#            fromStationTelecode = data_list[4]
#            toStationTelecode = data_list[5]
#            train_location = data_list[15]
#            leftTicket = data_list[12]
#            ticket = TicketModel(train_no,from_station_code,from_station_name,to_station_code,to_station_name
#               , start_time,arrive_time ,time_fucked_up,super_class_seat,first_class_seat,second_class_seat   ,
#               super_soft_sleep,soft_sleep,move_sleep,hard_sleep, hard_seat, no_seat,other,remind , 
#                train_no_Long,fromStationTelecode,toStationTelecode,train_location,leftTicket)
#            tickets.append(ticket.toArray())
#        return tickets
##            info = ('车次:{}\n出发站:{}\n目的地:{}\n出发时间:{}\n到达时间:{}\n消耗时间:{}\n座位情况：\n 特等座：「{}」 \n 一等座：「{}」 \n二等座：「{}」\n软卧：「{}」\n硬卧：「{}」\n硬座：「{}」\n无座：「{}] \n备注：{} \n\n'.format(
##                train_no, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up, super_class_seat,first_class_seat,
##                second_class_seat, soft_sleep, hard_sleep, hard_seat, no_seat,remind))
##            print (ticket.toArray())

def queryTicket(begin,des,goTime):
    tickets = []
    tickets2 = []
    global_dict ,global_dict_cn= queryCityMap()  
    if (len(begin) ==0) or ( len(des) ==0):
        print "请输入出发地 目的地!"
        return tickets,tickets2
    begin = global_dict_cn[begin]
    des = global_dict_cn[des]
    print 'queryTicket 出发地：{}  目的地：{} 时间： {}'.format(begin, des,goTime)
    r = getTrainNoList(goTime,goTime,begin,des)
    res =json.loads(r)
    if(res.get('httpstatus') == 200) :
        data = res.get('data')
        if data is None:
            return tickets,tickets2
        result = data.get('result')
        for d in result:
            data_list  = d.split('|')
#            for ss in data_list:
#                print(ss)
                    # 车次号码
            train_no = data_list[3]
                # 出发站
            from_station_code = data_list[6]
            from_station_name =global_dict[from_station_code]
                # 终点站
            to_station_code = data_list[7]
            to_station_name = global_dict[to_station_code]
                # 出发时间
            start_time = data_list[8]
                # 到达时间
            arrive_time = data_list[9]
                # 总耗时
            time_fucked_up = data_list[10]
                #商务特等座
            super_class_seat = data_list[32] or '--'
                # 一等座
            first_class_seat = data_list[31] or '--'
                # 二等座
            second_class_seat = data_list[30]or '--'
                #高级 软卧
            super_soft_sleep = data_list[22]or '--'
                # 软卧
            soft_sleep = data_list[23]or '--'
                # 动卧
            move_sleep = data_list[24]or '--'
                # 硬卧
            hard_sleep = data_list[28]or '--'
            # 硬座
            hard_seat = data_list[29]or '--'
                # 无座
            no_seat = data_list[26]or '--'
                #其他
            other = '--'
            #备注
            remind = data_list[1]
            #   火车票秘钥
            secretStr = data_list[0]
            train_no_Long = data_list[2]
            fromStationTelecode = data_list[4]
            toStationTelecode = data_list[5]
            train_location = data_list[15]
            leftTicket = data_list[12]
            ticket = TicketModel(train_no,from_station_code,from_station_name,to_station_code,to_station_name
               , start_time,arrive_time ,time_fucked_up,super_class_seat,first_class_seat,second_class_seat   ,super_soft_sleep,
               soft_sleep,move_sleep,hard_sleep, hard_seat, no_seat,other,remind,secretStr,
            train_no_Long,fromStationTelecode,toStationTelecode,train_location,leftTicket)
            tickets.append(ticket.toArray())
            tickets2.append(ticket)
        return tickets,tickets2
    
def queryMyNoCompleteOrder():
    result = queryMyOrderNoComplete()
    if result is None:
        return
    else:
        dic  = json.loads(result) 
        orderSet =[]
#        返回多张订单 这里目前先只处理 第一个订单
        if  dic.has_key("data") ==False:
            return
        for order_content in dic["data"]["orderDBList"]:
            sequence_no  = order_content["sequence_no"]
            order_date = order_content["order_date"]
            start_train_date_page = order_content["start_train_date_page"]
            
    #        num =  len(order_content["tickets"])
    #        一张订单可以有多张票
            for ticket in order_content["tickets"]:
                station_train_code = ticket["stationTrainDTO"]["station_train_code"]
                from_station_name = ticket["stationTrainDTO"]["from_station_name"]
                to_station_name =  ticket["stationTrainDTO"]["to_station_name"]
                passenger_name =   ticket["passengerDTO"]["passenger_name"]
                ticket_type_name = ticket["ticket_type_name"]
                seat_type_name = ticket["seat_type_name"]
                coach_name = ticket["coach_name"]
                seat_name =  ticket["seat_name"]
                str_ticket_price_page = ticket["str_ticket_price_page"]
                ticket_status_name =  ticket["ticket_status_name"]
                noOrder = TicketNoCompletOrder(sequence_no, order_date, start_train_date_page, station_train_code, from_station_name, to_station_name, 
                        passenger_name, ticket_type_name, seat_type_name, coach_name, seat_name, str_ticket_price_page, ticket_status_name)
                orderSet.append(noOrder.toArray())
        print orderSet
        return orderSet
def callBack():
    print('call back')
#mygui.showUI(query(),callBack)
#print(type(query()))
#print((query()))

