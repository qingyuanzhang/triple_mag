# -*- coding:utf8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import patterns, url

from TripleMag.apps.store.views import *

urlpatterns = patterns('',
    #报单首页
    url('store/$',index, name='store_index'),
    #账户充值
    url(r'store/charge/$',charge,name="store_charge"),
    #查看报单记录
    url('store/declare_records/$', declare_records,name="declare_records"),
    #查看货物列表
    url('store/stuff_list/$', stuff_list, name='stuff_list'),
    #查看货物的详情
    url('store/stuff_info/$',stuff_info, name="stuff_info"),
    #订货
    url(r'store/order/$',order, name="stuff_order"),
    #订货记录
    url(r'store/order_records/$',store_order_records,name="stuff_order_records" ),
    #查看自己添加的会员
    url(r'store/added_mem/$',added_mem,{'template_name':'store/store_base.html'},name="store_added_mem"),
    #添加地址
    url(r'store/add_address/$',address,name="store_add_address"),
    #删除地址
    url(r'store/del_address/$',del_address,name='store_del_address'),
)
urlpatterns += patterns('',
    #报单中心添加会员
    url(r'store/add_member_1/$','TripleMag.apps.management.views.add_member',{'template_name':'store/add_member.html'},name="store_add_member"),

)
