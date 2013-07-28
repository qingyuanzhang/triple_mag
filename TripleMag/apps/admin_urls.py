# -*- coding:utf8 -*-
from django.conf.urls.defaults import patterns, url, include
from TripleMag.apps import management,mall
from TripleMag.apps.views import *

urlpatterns = patterns('',

    url(r'/admin/index/$','TripleMag.apps.views.index',name='apps_index'),
#    url(r'management/',include(management.urls)),
#    url(r'get_user_name/',get_user_name),
)
