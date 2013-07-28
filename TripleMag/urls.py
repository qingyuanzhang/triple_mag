#coding=utf-8
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from TripleMag.apps import sites 
from Mall.engine.index import index
urlpatterns = patterns('',
       (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/usr/local/lib/python2.6/dist-packages/django/contrib/admin/media' }),
    # Examples:
    # Uncomment the next line to enable the admin:
#    url(r'^admin/', include(admin.site.urls)),
    (r'^$',index.index),
    url(r'^account/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', include('TripleMag.apps.management.urls')),
    url(r'^',include('TripleMag.apps.management.urls'),name='management'),
    url(r'^',include('TripleMag.apps.mall.urls')),
    url(r'^',include('TripleMag.apps.member.urls')),
    url(r'^',include('TripleMag.apps.money.urls')),
    url(r'^rt/',include("TripleMag.apps.urls")),
    url(r'^', include("TripleMag.apps.stock.urls")),
    #####test#####
#    url(r'',include(sites.urls)),
    url(r'^test/$','TripleMag.apps.views.test', name='test'),
    url(r'^mall/',include('Mall.urls')),
    url(r'^',include('TripleMag.apps.store.urls')),
    url(r'^announcements/',include("announcements.urls")),
    url(r'^notice/',include("notification.urls")),
    (r'^malltest/$','direct_to_template', {'template': 'mall/mall_test.html'}),
    url(r'^rt_test/$','TripleMag.apps.views.test'),

)
