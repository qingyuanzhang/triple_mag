from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required
@login_required
def urls(request,role = None):
    site_map = {
        'admin': include('TripleMag.apps.admin_urls'),
#        'member': include('TripleMag.apps.member_urls'),
#        'store': include('TripleMag.apps.store_urls'),
#        'mall_user': include('TripleMag.apps.mall_user_urls')
    }
    
    urlpatterns = patterns('',
            url(r'rentai/',include('TripleMag.apps.admin_urls'),name="tt"),
            )
    return urlpatterns
