# -*- coding:utf8 -*-
from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
#from TripleMag.models import model
from TripleMag.apps.member.views import *
from TripleMag.apps.management.views import announcements_list
from django.views.decorators.cache import cache_page
urlpatterns = patterns('',
    url(r'member/member_details/$',member_details,{'template_name': 'member/member.html'},name='member_details',),#管理员和报单中心根据自己的角色查看会员信息
    url(r'member/change_info/$',change_info),#修改个人信息
    url(r'member/change_info_appl/$',change_info_appl,name="mem_change_info_appl"),#个人信息修改申请
    url(r'member/upgrade_appl/$', upgrade_appl_index, name='mem_upgrade_appl'),#会员升级申请
    url(r'member/file_download/$', file_download,{'template_name':'member/file_download.html'}, name='file_download'),#资料下载
    url(r'download', download, name='download'),#下载
    #查看公告列表
    url(r'member/announcements_list/$',announcements_list, { 'template_name': 'member/announcements_list.html','banner':'member/banner_main.html' },name="mem_announcements_list"),
    #查看公告详细信息
    url(r'member/announcements_list/', announcements_list,{ 'template_name' : 'member/announcements_list.html','banner':'member/banner_main.html' },name='mem_announcements_detail'),
    #会员的首页
    
    url(r'member/$', index, name='member'),
    #会员信息和电子银行首页
    url(r'member/index/$', member_details, {'template_name':'member/member.html'},name="member_index"),
    #留言板
    url(r'member/leave_messages/$',messages, name='member_messages'),
    url(r'^member/bonus_center/$',bonus_center,name="member_bonus_center"),
    #查看奖金记录
    url(r'^member/bonus_a/$', a_bonus,{'include_template':'includes/counter_detail.html','bonus_style':'a_bonus'},name ='member_a_bonus'),
    
    url(r'^member/bonus_c/$',a_bonus,{'include_template':'includes/c_counter_detail.html','bonus_style':'c_bonus'},name ='member_c_bonus'),
    #不发放奖金的查看
    url(r'^member/unpaid_bonus/$',unpaid_bonus,{'template_name':'member/extra_bonus.html'},name="unpaid_bonus"),
    #地址管理
    url(r'^member/manage_addr/$',manage_address,{'template_name':'member/manage_address.html'},name="manage_address"),
    
    url(r'member/share_appl/$',mem_share_appl,name="mem_share_appl"),
    #申请成为VIP
    url(r'member/vip_appl/$',mem_vip_appl,name="mem_vip_appl"),
    #会员查看自己的三代接点人关系修改url
    url(r'member/conactor/$',mem_conactor,name="mem_conactor"),
    
)

urlpatterns += patterns('',
    #产品销售奖金明细查看
    url(r'member/a_bonus_detail/$',"TripleMag.apps.management.views.a_bonus_detail",{'template_name':'member/a_bonus_detail.html','bonus_style':'a_bonus','sub_website':"产品销售"},name = "member_a_bonus_detail"),
    url(r'member/c_bonus_detail/$',"TripleMag.apps.management.views.a_bonus_detail",{'template_name':'member/a_bonus_detail.html','bonus_style':'c_bonus','sub_website':"商城"},name = "member_c_bonus_detail"),
)
