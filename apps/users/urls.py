# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('users.views',
    (r'^sessionexam/(?P<exam_id>\d+)/$', 'session',),
)


