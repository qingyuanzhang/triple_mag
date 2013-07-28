# -*- coding:utf8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
#from TripleMag.models import model
from TripleMag.apps.stock.views import *


urlpatterns = patterns('',
    #股票首页
    url(r'stock/$',index,name='stock_index'),
    #非定向购买股票
    url(r'stock/buy$',buy_stock, name = "stock_buy_stock"),
    #卖出股票
    url(r'stock/sell/$', sell_stock , name = "stock_sell_stock"),
    #实时刷新卖出池
    url(r'stock/get_selling_poll/$', get_selling_poll, name = "get_selling_poll"),
    #查看自己的股票来源
    url(r'stock/income_record/$', income_record,{'template_name':'stock/stock_record.html'}, name="stock_income_record"),
    #查看自己的购票售出记录
    url(r'stock/stock_record/$',stock_record,{'template_name':'stock/stock_record.html','include_template':'includes/stock_record.html'},name="stock_stock_record"),
    #查看自己的股票奖金记录
    url('stock/stock_bonus/$',stock_bonus,{'template_name':'stock/stock_record.html','include_template':'includes/stock_bonus.html'},name="stock_stock_bonus"),
    #取消自己的股票
    url(r'stock/cancle/$',cancle_stock,name="cancle_stock"),
    #定向购买
    url(r'stock/direct_buy/$',direct_stock_buy,name="direct_stock_buy"),
    url(r'stock/del_session/$',del_session,name="del_session"),
)

