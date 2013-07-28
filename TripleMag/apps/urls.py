# -*- coding:utf8 -*-
from django.conf.urls.defaults import patterns, url, include
from TripleMag.apps import management,mall
from TripleMag.apps.views import *

urlpatterns = patterns('',

    url(r'index/$','TripleMag.apps.views.index',name='apps_index'),
    url(r'get_user_name/$',get_user_name ,name="get_user_name"),
    url(r'change_one/$',change_one,name="change_one"),
    url(r'change_number/$',change_number, name="change_number"),
    url(r'out_put_csv/$',out_put_csv,name="out_put_csv"),
    url(r'upload_image/$',upload_image,name="upload_image"),
    url(r'check_existing/$',check_existing,name='check_existing'),
)

#admin url 


