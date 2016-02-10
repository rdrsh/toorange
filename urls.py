# -*- coding: utf-8 -*- 

from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from django.conf import settings
SR = settings.STATIC_ROOT

urlpatterns = patterns('',)

urlpatterns += patterns('',
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('main.views',
    (r'^$', 'index'),
    (r'^faq/$', 'faq'),
    (r'^buy/$', 'buy'),
    (r'^events/$', 'events'),
    (r'^events/(\d+)/$', 'events'),
    (r'^facts/$', 'facts'),
    (r'^facts/(\d+)/$', 'facts'),
    (r'^products/$', 'products'),
    (r'^products/(\d+)/$', 'products'),
    (r'^contact/$', 'contact'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^404/$', 'main.views._404'),
        (r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': SR+'/img/'}),
        (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': SR+'/js/'}),
        (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': SR+'/css/'}),
    )

urlpatterns += patterns('main.views',
    (r'^([\-\d\w]+)/$', 'page'),
    (r'^([\-\d\w]+)/([\-\d\w]+)/$', 'page'),
)

