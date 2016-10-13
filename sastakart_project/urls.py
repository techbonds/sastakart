from django.conf.urls import patterns,include, url
from django.contrib import admin
from sastakart.views import *


# admin.autodiscover()
urlpatterns = patterns('',    
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('sastakart.urls',namespace='sastakart')),
    url(r'^admin/', include(admin.site.urls)),    
) 
