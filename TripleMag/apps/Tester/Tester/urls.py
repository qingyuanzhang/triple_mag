from django.conf.urls import patterns, include, url
from view import current_datetime
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #(r'^time/$', current_datetime),
    # Examples:
    # url(r'^$', 'Tester.views.home', name='home'),
    # url(r'^Tester/', include('Tester.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
