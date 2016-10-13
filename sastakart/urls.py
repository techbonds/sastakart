from django.conf.urls import patterns, include, url
from django.contrib import admin
from sastakart.views import *


urlpatterns = patterns('',
    url(r'^$', SearchFormView.as_view(), name='home'),
    url(r'^searchbar/$', SearchBarView.as_view(), name='searchbar'),
    url(r'^search/(?P<keyword>[a-zA-Z0-9!@#$&()\\ -`.+,/\"]*)/(?P<page>[0-9]*)/$', SearchResultView.as_view(), name='search'),
    url(r'^product/(?P<epid>[a-zA-Z0-9!@#$&()\\ -`.+,/\"]*)/$', ProductView.as_view(), name='product'),
    url(r'^faq/$',FAQView.as_view(),name='faq'),
    url(r'^contact/$',ContactView.as_view(),name='contact'),
    url(r'^about/$',AboutView.as_view(),name='about'),    
   	)
