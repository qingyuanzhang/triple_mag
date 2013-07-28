# -*- coding:utf8 -*-
from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
#from TripleMag.models import model
from TripleMag.apps.management.views import *
from TripleMag.apps.store.views import store_order_records

from django.views.decorators.cache import cache_page

urlpatterns = patterns('',
    #添加会员
    url(r'management/add_member/$',add_member,{'template_name':'management/member/add_member.html'}, name='management_add_member'),
    #查看报单中心添加的会员
    
    url(r'management/added_mem/$',"TripleMag.apps.store.views.added_mem",{'template_name':'management/member/added_mem.html'},name="management_added_mem"),
    #搜索会员
    url(r'management/serach/$',search_member,name='management_search_member'),
    #开通会员申请
    url(r'management/member/(?P<choices>)/$', allow_or_reject, name="management_allow_or_reject"),
    #申请中心
    url(r'management/application/$', application,name= "management_application"),
    #搜索商品
    #处理会员的VIP申请
    url(r'management/deal_memmin_upgrade_appl/$',deal_memmin_upgrade_appl,name="deal_memmin_upgrade_appl"),
    
    #添加商品
    url(r'management/add_product/$',add_product,name="management_add_product"),
    #添加商品的类型
    url(r'management/add_stuff_type/$',add_stuff_type,name="management_add_stuff_type"),
    #给现金/报单账户充值
    url(r'management/charge/$',charge,name="management_charge"),
    #ajax进行充值
    url(r'management/charge_now/$',to_charge,name = 'charge_now'),
    #对用户的修改申请进行处理
    url(r'management/del_appl/$',del_appl),
    #对会员的状态进行更改
    url(r'management/change_state/$', change_state, name='change_state'),
    #查看报单中心申请
    url(r'management/upgrade_appl_info/$', upgrade_appl_info,name='management_upgrade_appl'),
    #ajax会员升级
    url(r'management/upgrade/$', allow_appl, name='management_upgrade'),
    #会员提现列表
    url(r'management/withdraw_appl/$', withdraw_appl, name ='management_withdraw_appl'),
    #允许或拒绝会员提现申请
    url(r'management/del_withdraw_appl/$', deal_withdraw_appl, name = 'deal_withdraw_appl'),
    #查看会员的汇款帐号
    url(r'management/bank_info/$', bank_info, name = 'bank_info'),
    #管理货物类型 
    url(r'management/manage_stuff_type/$', manage_stuff_type, name='manage_stuff_type'), 
    #删除货物类型
    url(r'management/del_stuff_type/$',del_stuff_type,name = 'del_stuff_type'),
    #修改货物类型信息
    url(r'management/change_stuff_type/$',change_stuff_type,name = 'change_stuff_type'),
    #添加货物类型
    url(r'management/add_stuff_type/$', add_stuff_type, name='add_stuff_type'),
    #管理货物
    url(r'management/manage_stuff/$', manage_stuff, name="manage_stuff"),
    #删除货物
    url(r'management/del_stuff/$',del_stuff, name="del_stuff"),
    #增加货物
    url(r'management/add_stuff/$', add_stuff, name="add_stuff"),
    #修改货物属性
    url(r'management/change_stuff/$', change_stuff, name='change_stuff'),
    #查看所有的报单中心的订货记录
    url(r'management/store_order_records/$',store_order_records, name="manage_store_order_records"),
    #资料上传
    url(r'management/upload_file/$', upload_file, name="upload_file"),
    #发布公告
    url(r'management/public_announcements/$', public_announcements, name="public_announcements"),
    #查看公告列表
    url(r'^management/announcements_list/$',announcements_list, { 'template_name': 'management/sys/announcement_list.html' },name="announcements_list"),
    #管理公司公告
    url(r'management/manage_announcement/$',manage_announcement,name="manage_announcement"),
    #管理员首页
    url(r'^management/$',index,name = "management_index"),
    #会员和报单中心管理首页
    url(r'^management/member/$', member, name="management_member_index"),
    #系统管理首页
    url(r'^management/sys/$',sys_index,name="management_sys_index"),
    #股票管理首页
    url(r'^management/stock/$',stock_index,name='management_stock_index'),
    #商城管理首页
    url(r'^management/mall/$',mall_index,name="management_mall_index"),
    #添加商品的目录
#    url(r'^management/mall/manage_catagory/$',manage_catagory, name="management_manage_catagory"),
    
    #空点会员列表
    url(r'^management/member_void/$',member_void,name="member_void"), 
    #提现记录
    url(r'management/withdraw_record/$','TripleMag.apps.money.views.withdraw_record',name='management_withdraw'),
    #转帐记录
    url(r'management/trans_records/$','TripleMag.apps.money.views.trans_records',name="management_trans_records"),
    #产品销售奖金结算
    url(r'^management/a_bonus_settlement/$',a_bonus_settlement, name="a_bonus_settlement"),
    #C网结算并发放
    url(r'management/c_bonus_settlement/$',c_bonus_settlement,name="c_bonus_settlement"),
#    #产品销售奖金发放
#    url(r'management/a_bonuses/$',a_bonuses, name="a_bonuses"),
    #产品销售每期奖金查看
    url(r'management/a_bonus_counter/$',a_bonus_counter,{'bonus_style':'a_bonus'},name="management_a_bonus_counter"),
    #C网每期奖金查看
    url(r'management/c_bonus_counter/$',a_bonus_counter,{'bonus_style':'c_bonus'},name="management_c_bonus_counter"),
    
    #查询
    url(r'management/search/$','search_member', name = 'admin_search'),
    #每天的业绩累计
    url(r'management/day_perform_record/$',day_perform_record,{'template_name':'management/member/day_perform_record.html'},
        name="management_day_perform_record"),
    #删除用户
    url(r'management/delete_member/$',delete_member,name="delete_member"),
    #查看3代推荐人
    url(r'management/recommender/$', recommender, name="management_recommender"),
    #奖金明细查看
    url(r'management/a_bonus_detail', a_bonus_detail,{'template_name':'management/member/a_bonus_detail.html','bonus_style':'a_bonus','sub_website':'产品销售'}, name="management_a_bonus_detail"),
    #奖金明细查看
    url(r'management/c_bonus_detail', a_bonus_detail,{'template_name':'management/member/a_bonus_detail.html','bonus_style':'c_bonus','sub_website':'商城'}, name="management_c_bonus_detail"),
    #功能开关
    url(r'management/function_switch/$',function_switch,name='function_switch'),
    #产品销售数值设定
    url(r'management/a_web_value_setting',a_web_value_setting,name='a_web_value_setting'),
    #C网数值设定
    url(r'management/c_web_value_setting',c_web_value_setting,name='c_web_value_setting'),
    #接点人业绩查看表
    url(r'management/contacting_chart/$',contacting_chart,name='contacting_chart'),
)
urlpatterns += patterns('',
    #回复留言
    url(r'management/reply/$',"TripleMag.apps.member.views.reply",{'base':'management/base.html'},name="admin_reply"),
    #管理员查看留言
    url(r'management/messages/$',"TripleMag.apps.member.views.messages", {'template_name':'management/sys/messages.html'},name="admin_messages"),
    #删除留言
    url(r'^management/message_del/$',message_del,name='message_del'),
    #查看会员详情
    url(r'management/member_detail/$', "TripleMag.apps.member.views.member_details",{'template_name':'management/member/member_details.html'}, name="management_member_detail"),
    #修改会员的信息
    url(r'management/change_mem_info/$', "TripleMag.apps.member.views.member_details",{'template_name':'management/member/change_mem_info.html'}, name="management_change_mem_info"),
    #查看股票的交易记录
    url(r'management/stock_record/$',"TripleMag.apps.stock.views.stock_record",{'template_name':'management/stock/stock_record.html'},name="management_stock_record"),
    #查看股票的奖金记录
    url(r'management/stock_bonus/$',"TripleMag.apps.stock.views.stock_bonus",{'template_name':'management/stock/stock_record.html'},name="management_stock_bonus"),
    #股票来源记录
     url(r'management/income_record/$', "TripleMag.apps.stock.views.income_record",{'template_name':'management/stock/stock_record.html'}, name="management_income_record"),
    #资料列表
    url(r'management/file_list/$',"TripleMag.apps.member.views.file_download",{'template_name':'management/sys/file_download.html'},name="management_file_list"),
    #资料修改和删除
    url(r'management/file_change/$',file_change,{'template_name':'management/sys/file_change.html'},name="file_change"),
    #万能搜索页面
    url(r'^management/search_fuc/$',search_fuc,name="search_fuc"),
    #导出文件
    url(r'^out_put_csv/$',out_put_csv,name="out_put_csv"),
    #重置密码
    url(r'^management/reset_password/$',reset_password,name="reset_password"),
    #拨出率统计表
    url(r'^management/extracting_rate/$',extracting_rate,name="extracting_rate"),
    #管理员登录会员的界面
    url(r'^management/login_mem',management_login_mem,name="management_login_mem"),
)

urlpatterns += patterns("",

    url(r"management/clean_data/$",clean_data,name="clean_data"),
    url(r"management/test_data/$",test_data,name="test_data"),
    url(r'management/make_day_check/$',make_day_check,name="make_day_check"),
    url(r'management/extra_bonus/$',"TripleMag.apps.member.views.unpaid_bonus",{'template_name':"management/member/extra_bonus.html"},name="management_extra_bonus"),
)




