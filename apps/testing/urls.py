# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('testing.views',
    (r'^sessionexam/(?P<sessionexam_id>\d+)/$', 'sessionexam',),
)

