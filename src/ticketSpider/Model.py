#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017-9-12

@author: miaoxu
'''
class TicketModel(object):
    '''
    classdocs
    '''


    def __init__(self,train_no,from_station_code,from_station_name,to_station_code,to_station_name
               , start_time,arrive_time ,time_fucked_up,super_class_seat,first_class_seat,second_class_seat   ,
               super_soft_sleep,soft_sleep,move_sleep,hard_sleep, hard_seat, no_seat,other,remind,secretStr,
               train_no_Long,fromStationTelecode,toStationTelecode,train_location,leftTicket):
             
        self.train_no = train_no
        self.from_station_code = from_station_code
        self.from_station_name = from_station_name
        self.to_station_code = to_station_code
        self.to_station_name = to_station_name
        self.start_time = start_time
        self.arrive_time = arrive_time
        self.time_fucked_up = time_fucked_up
        self.super_class_seat = super_class_seat
        self.first_class_seat = first_class_seat
        self.second_class_seat = second_class_seat
        self.super_soft_sleep = super_soft_sleep
        self.soft_sleep = soft_sleep
        self.move_sleep = move_sleep
        self.hard_sleep = hard_sleep
        self.hard_seat = hard_seat
        self.no_seat = no_seat
        self.other = other
        self.remind = remind
        self.secretStr = secretStr
        self.train_no_Long = train_no_Long
        self.fromStationTelecode = fromStationTelecode
        self.toStationTelecode = toStationTelecode
        self.train_location = train_location
        self.leftTicket = leftTicket
    def toArray(self):
        return [ self.train_no,self.from_station_name+'/'+self.to_station_name,self.start_time+'/'+self.arrive_time 
                    , self.time_fucked_up, self.super_class_seat,self.first_class_seat, self.second_class_seat, self.super_soft_sleep,self.soft_sleep,self.move_sleep
                    ,self.hard_sleep,  self.hard_seat, self.no_seat,self.other, self.remind,self.secretStr,self.fromStationTelecode, self.toStationTelecode
                    ,self.train_location, self.leftTicket,self.train_no_Long ]
        
'''
Created on 2017-9-19

@author: miaoxu
'''
class  PassengersModel(object):
    def __init__(self,passenger_name,code,sex_code,sex_name,born_date,passenger_id_type_code,
                 passenger_id_type_name,passenger_id_no,passenger_type,passenger_type_name,mobile_no):
        self.passenger_name = passenger_name
        self.code =code
        self.sex_code = sex_code
        self.sex_name = sex_name
        self.born_date = born_date
        self.passenger_id_type_code = passenger_id_type_code
        self.passenger_id_type_name = passenger_id_type_name
        self.passenger_id_no = passenger_id_no
        self.passenger_type = passenger_type
        self.passenger_type_name = passenger_type_name
        self.mobile_no = mobile_no
    
    def toArray(self):
        return [self.passenger_name, self.code,  self.sex_code,self.sex_name, self.born_date ,
                 self.passenger_id_type_code , self.passenger_id_type_name , self.passenger_id_no ,self.passenger_type,self.passenger_type_name ,
                  self.mobile_no 
                 ]
'''
'''  
class TicketNoCompletOrder():
    def __init__(self,sequence_no,order_date,start_train_date_page,station_train_code,
                 from_station_name,to_station_name,passenger_name,ticket_type_name,seat_type_name,
                 coach_name,seat_name,str_ticket_price_page,ticket_status_name):
        self.select = '选择'
        self.sequence_no = sequence_no
        self.order_date = order_date
        self.start_train_date_page = start_train_date_page
        self.station_train_code = station_train_code
        self.from_station_name =from_station_name
        self.to_station_name = to_station_name
        self.passenger_name = passenger_name
        self.ticket_type_name = ticket_type_name
        self.seat_type_name = seat_type_name
        self.coach_name = coach_name
        self.seat_name = seat_name
        self.str_ticket_price_page = str_ticket_price_page
        self.ticket_status_name = ticket_status_name
        
    def toArray(self):
        return [self.select , self.sequence_no,self.order_date, self.start_train_date_page, self.station_train_code,
                  self.from_station_name ,self.to_station_name ,   self.passenger_name,  self.ticket_type_name,   
                     self.seat_type_name ,  self.coach_name,       self.seat_name , self.str_ticket_price_page,self.ticket_status_name
                 ]
        
class TicketCompletOrder():
    pass 

class MyAccountOrder():
    pass