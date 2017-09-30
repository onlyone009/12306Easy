#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017-9-21

@author: miaoxu
'''
from wx._core import BoxSizer, wx
from msilib.schema import RadioButton
from wx._windows import Panel
from wx.grid import Grid, PyGridCellRenderer, GridCellAttr, PyGridTableBase
import random
from ticketSpider.TicketAPI import mySession, queryMyOrderNoComplete
import threading
from gui.queryTicketParser import queryMyNoCompleteOrder
import webbrowser
"""
订单管理页面sizer 有问题 无法使用
"""
class OrderManagerSizer(BoxSizer):
    '''
    classdocs
    '''


    def __init__(self, panel,*args, **kwargs):
        BoxSizer.__init__(self, *args, **kwargs)
        self.panel = panel 
        self.top_staticbox_1 = wx.StaticBox(self.panel, -1, "操作")
        self.top_staticbox_2 = wx.StaticBox(self.panel, -1, "未完成订单")
        self.top_staticbox_3 = wx.StaticBox(self.panel, -1, "已完成订单")
        self.__do_layout()
    def __do_layout(self):
        self.top_staticbox_1.Lower()
        self.top_staticbox_2.Lower()
        self.top_staticbox_3.Lower()
        self.sizer_top_staticBoxSizer_1 =   wx.StaticBoxSizer(self.top_staticbox_1, wx.HORIZONTAL)
        self.sizer_top_staticBoxSizer_2 =   wx.StaticBoxSizer(self.top_staticbox_2, wx.HORIZONTAL)
        self.sizer_top_staticBoxSizer_3 =   wx.StaticBoxSizer(self.top_staticbox_3, wx.HORIZONTAL)
        
        sizer_top = wx.BoxSizer(wx.HORIZONTAL)
        sizer_top.Add( self.sizer_top_staticBoxSizer_1,1,wx.EXPAND, 0)
        sizer_top.Add( self.sizer_top_staticBoxSizer_2,1,wx.EXPAND, 0)
        sizer_top.Add(self.sizer_top_staticBoxSizer_3,1,wx.EXPAND, 0)

"""
订单管理页面Pannel
"""    
class OrderManagerPanel(Panel):
    '''
    classdocs
    '''
    def __init__(self,*args, **kwargs):
        Panel.__init__(self, *args, **kwargs)
        self.top_staticbox_1 = wx.StaticBox(self, -1, "操作")
        self.top_staticbox_2 = wx.StaticBox(self, -1, "未完成订单")
        self.top_staticbox_3 = wx.StaticBox(self, -1, "已完成订单")
        
        self.btn_queryOoders = wx.Button(self, -1, u'查询全部订单',size=(200,-1))
        self.btn_payOrder = wx.Button(self, -1, u'继续支付')
        self.btn_cancelOrder = wx.Button(self, -1, u'取消订单')
        self.btn_fadeTicket = wx.Button(self, -1, u'退票')
        self.btn_changeTicket = wx.Button(self, -1, u'改签(刷票)')
        self.btn_changeDes = wx.Button(self, -1, u'变更到站(刷票)')
        
        self.data_grd = Grid(self, -1, size=(1, 1))
        
        self.__set_properties()
        self.__do_layout()
        self.__bindBtinEvent()
    def __set_properties(self):
        
        self.data_grd.CreateGrid(10, 13)
        self.data_grd.SetRowLabelSize(30)
        self.data_grd.SetColLabelSize(30)
        self.data_grd.EnableEditing(0)
        self.data_grd.HideRowLabels()#隐藏自动生成的序号
        self.data_grd.SetLabelBackgroundColour(wx.Colour(127, 193, 255))
        self.data_grd.SetColLabelValue(0, "选择")
        self.data_grd.SetColLabelValue(1, "订单号")
        self.data_grd.SetColLabelValue(2, "订单时间")
        self.data_grd.SetColLabelValue(3, "发车时间")
        self.data_grd.SetColLabelValue(4, "车次")
        self.data_grd.SetColLabelValue(5, "发站")
        self.data_grd.SetColLabelValue(6, "到站")
        self.data_grd.SetColLabelValue(7, "乘客")
        self.data_grd.SetColLabelValue(8, "票种")
        self.data_grd.SetColLabelValue(9, "席别")
        self.data_grd.SetColLabelValue(10, "车厢")
        self.data_grd.SetColLabelValue(11, "座位")
        self.data_grd.SetColLabelValue(12, "票价")
        self.data_grd.SetColLabelValue(12, "状态")
    def __bindBtinEvent(self):      
        self.Bind(wx.EVT_BUTTON, self.onbtn_queryOoders, self.btn_queryOoders)
        self.Bind(wx.EVT_BUTTON, self.fun_jump_pay, self.btn_payOrder)
        
    def onbtn_queryOoders(self,event):
        t1 = threading.Thread(target=self.fun_thread_queryMyNoCompleteOrder)
        t1.start()
        
    def fun_thread_queryMyNoCompleteOrder(self):
        result = queryMyNoCompleteOrder()
        self.data = GridData2(result)
        self.data_grd.SetTable(self.data)
        self.data_grd.Refresh()
      
    def fun_jump_pay(self,event):
        webbrowser.open_new_tab('https://kyfw.12306.cn/otn/queryOrder/initNoComplete')
        
    def __do_layout(self):
        self.top_staticbox_1.Lower()
        self.top_staticbox_2.Lower()
        self.top_staticbox_3.Lower()
        self.sizer_top_staticBoxSizer_1 =   wx.StaticBoxSizer(self.top_staticbox_1, wx.HORIZONTAL)
        self.sizer_top_staticBoxSizer_2 =   wx.StaticBoxSizer(self.top_staticbox_2, wx.HORIZONTAL)
        self.sizer_top_staticBoxSizer_3 =   wx.StaticBoxSizer(self.top_staticbox_3, wx.HORIZONTAL)
        
#        整个容器
        sizer_whole= wx.BoxSizer(wx.VERTICAL)
#        上方容器
        sizer_top = wx.BoxSizer(wx.HORIZONTAL)
#        下方容器
        sizer_bottom = wx.BoxSizer(wx.HORIZONTAL)
        
        self.sizer_top_staticBoxSizer_1.Add(self.btn_queryOoders,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,7) 
        self.sizer_top_staticBoxSizer_2.Add(self.btn_payOrder,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,7) 
        self.sizer_top_staticBoxSizer_2.Add(self.btn_cancelOrder,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,7) 
        self.sizer_top_staticBoxSizer_3.Add(self.btn_fadeTicket,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,7) 
        self.sizer_top_staticBoxSizer_3.Add(self.btn_changeTicket,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,7) 
        self.sizer_top_staticBoxSizer_3.Add(self.btn_changeDes,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,7) 
        
        sizer_top.Add( self.sizer_top_staticBoxSizer_1,0,wx.EXPAND|wx.RIGHT,7)  
        sizer_top.Add( self.sizer_top_staticBoxSizer_2,0,wx.EXPAND |wx.RIGHT,7) 
        sizer_top.Add(self.sizer_top_staticBoxSizer_3,0,wx.EXPAND|wx.RIGHT,7) 
        
        sizer_bottom.Add( self.data_grd,1,wx.EXPAND,0)
        
        sizer_whole.Add(sizer_top,1,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM,7)   
        sizer_whole.Add(sizer_bottom,7,  wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,7)   
        
        self.SetSizer(sizer_whole)

#表格数据实体类 必须重写一个PyGridTableBase
class GridData2(PyGridTableBase):
    _cols = "选择 订单号 订单时间 发车时间 车次 发站 到站 乘客 票种 席别  车厢  座位 票价  状态" .split()
    _data = [
            "1 2 3".split(),
            "4 5 6".split(),
            "7 8 9".split()
            ]
    _highlighted = set()
    def __init__(self, data):
        PyGridTableBase.__init__(self)
        self._data = data or[]

    def GetColLabelValue(self, col):
        return self._cols[col]

    def GetNumberRows(self):
        return len(self._data)

    def GetNumberCols(self):
        return len(self._cols)

    def GetValue(self, row, col):
        return self._data[row][col]

    def SetValue(self, row, col, val):
        self._data[row][col] = val

    def GetAttr(self, row, col, kind):
        attr = GridCellAttr()
        if(row%2==0):
            attr.SetBackgroundColour(wx.WHITE)
        else:
            attr.SetBackgroundColour(wx.WHITE)
            
#        if(col == 0 ):
##            attr.SetBackgroundColour( )   
##            attr.SetTextColour(wx.Colour(127, 193, 255))
#            font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
#            font.SetUnderlined(True)
#            attr.SetFont(font)
#            attr.SetTextColour(wx.Colour(127, 193, 255))
#        elif ( "预订"  in  self._data[row][col] ) and  ( col == (len(self._cols)-1) ) :
#            font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
#            font.SetUnderlined(True)
#            attr.SetFont(font)
#            attr.SetTextColour(wx.Colour(127, 193, 255))
        return attr

    def set_value(self, row, col, val):
        self._highlighted.add(row)
        self.SetValue(row, col, val)
            
"""
表格渲染器 渲染最后一列的颜色
"""
class  LastItemBtnRenderer(PyGridCellRenderer):
    def __init__(self):
        PyGridCellRenderer.__init__(self)
        
    def Draw(self, grid, attr, dc, rect, row, col, isSelected):#绘制
#        text = grid.GetCellValue(row, col)
#        if "预定" in text:
#        dc.SetTextBackground("blue")
        text = grid.GetCellValue(row, col)
        hAlign, vAlign = attr.GetAlignment()
        dc.SetFont( attr.GetFont() )
        if isSelected:
            bg = grid.GetSelectionBackground()
            fg = grid.GetSelectionForeground()
        else:
            bg = random.choice(["sky blue"])
            fg = attr.GetTextColour()
        dc.SetTextBackground(bg)
        dc.SetTextForeground(fg)
        dc.SetBrush(wx.Brush(bg, wx.SOLID))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangleRect(rect)
        grid.DrawTextRectangle(dc, text, rect, hAlign, vAlign)
    
    def GetBestSize(self, grid, attr, dc, row, col):
        text = grid.GetCellValue(row, col)
        dc.SetFont(attr.GetFont())
        w, h = dc.GetTextExtent(text)
        return wx.Size(w, h)
    
    def Clone(self):
        return LastItemBtnRenderer()