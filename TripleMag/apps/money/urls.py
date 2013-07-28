# -*- coding:utf8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import patterns, url
#from TripleMag.models import model
from TripleMag.apps.money.views import *
from TripleMag.apps.money.models import bonus_declare_record,bonus_mall_record
urlpatterns = patterns('',
    #现金中心首页
    url(r'money/$','TripleMag.apps.money.views.index',name='money_index'),
    #账户查看
    url(r'money/accounts/$','TripleMag.apps.money.views.accounts',{"template_name": "money/accounts.html"} ,name="money_accounts"),
    #提现申请
    url(r'money/withdraw/$',withdraw, name="money_withdraw"),
    #现金互转 
    url(r'money/trans/$',trans, name="money_trans"),
    #互转记录
    url(r'money/trans_records/$',trans_records,name="money_trans_records"),
    #用户提现记录
    url(r'money/withdraw_record/$',withdraw_record,name="money_withdraw_record"),
    #产品销售奖金发放记录表
    url(r'money/a_bouns_records/$',bonus_records,{'template_name':'money/a_bonus_records.html'},name = "a_bouns_records"),
    #C网奖金发放记录表
    url(r'money/c_bouns_records/$',bonus_records,{'template_name':'money/c_bonus_records.html'},name = "c_bouns_records"),
)

