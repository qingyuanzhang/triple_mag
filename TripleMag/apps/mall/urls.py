# -*- coding:utf8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import patterns, url
from TripleMag.apps.mall.models import Category,CategoryFirst,CategorySecond,Product,mall_index,mall_ad
from TripleMag.apps.management.models import notice_mall
from TripleMag.apps.mall.views import *
from TripleMag.apps.mall.forms import MallIndexForm,MallAdForm,NoticeMallForm


urlpatterns = patterns('',
    url(r'mall_management/$', index,{'template_name':'mall/mall_base.html'},'mall_management_index'),
 url(r'^category_change/$',change_category,name = "change_category"),
    url(r'mall_management/category_index/$',category_index,{'template_name':'management/mall/mall_index_mag.html'},name='mall_category_index'),
    url(r'^mall_management/delete_category_1st/(?P<c_id>.*)/$',delete_category,{'model':Category}),
    url(r'^mall_management/delete_category_2nd/(?P<c_id>.*)/$',delete_category,{'model':CategoryFirst}),
    url(r'^mall_management/delete_category_3rd/(?P<c_id>.*)/$',delete_category,{'model':CategorySecond}),
    #删除产品
    url(r'^mall_management/delete_product/(?P<p_id>.*)/$',delete_category,{'model':Product}),
    #商城主页设置
    url(r'^mall_home_mag/(?P<del_id>.*)$',mall_home_mag,{'model':mall_index,'form':MallIndexForm,'template_name':'management/mall/mall_home_mag.html'},name="mall_home_mag"),
    #商城推广设置
    url(r'^mall_ad/(?P<del_id>.*)$',mall_home_mag,{'model':mall_ad,'form':MallAdForm,'template_name':"management/mall/mall_ad.html"},name="mall_ad"),
    #添加商城首页图片
    url(r'add_home_mag/$',add_home_mag,name="add_home_mag"),
    #添加商城公告
    url(r'add_mall_notice/$',add_mall_notice,name="add_mall_notice"),
    #添加商城推广
    url(r'add_mall_ad/$',add_mall_ad,name="add_mall_ad"),
    
    #商城公告设置
    url(r'^mall_notice/(?P<del_id>.*)$',mall_home_mag,{'model':notice_mall,'form':NoticeMallForm,'template_name':"management/mall/mall_new_Announcement.html"},name="mall_notice"),
    url(r'^mall_management/product_list/$',product_list,{'template_name':'management/mall/product_list.html'},name='product_list'),
    url(r'mall_management/category/(?P<style>.*)/$', category,name = "mall_category"),
#    url(r'mall_management/category/add/(?P<style>.*)/$',add_category, name="mall_add_category"),
#    url(r'mall_management/delete_category/(?P<category_id>.*)$', delete_category, name="mall_delete_category"),
    url(r'manage_product/$',manage_product,name='manage_product'),
    url(r'mall_collection/$',mall_collection,name='mall_collection'),
    url(r'mall_register/$',register,name='mall_register'),
    url(r'orders/$',order_management,name="order_management"),
    url(r'change_password/$',change_password,name="change_password"),
    #我的收藏界面
    url(r'my_collections/$',my_collections,name="my_collections"),
    url(r'^comment/(?P<shop_record_id>.*)/$',comment,name="comment"),
    url(r'^search/$',search,name="search"),
    url(r'^change_mall_announcement/$',change_mall_announcement,name="change_mall_announcement"),
    url(r'^mall_notice_detail/$',mall_notice,name="mall_notice"),
    url(r'^order_cancle/$',cancle_order,name="cancle_order"),
)
#urlpatterns = patterns('',

#    url(r'^webshop/$','TripleMag.')


#)
