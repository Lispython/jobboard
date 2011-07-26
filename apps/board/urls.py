# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('board.views',
    url(r'^$', 'index', name="index"),
    url(r'^category/(?P<cat_id>\d+)/jobs', 'category', name="category"),
    url(r'^type/(?P<type_id>\d+)/jobs', 'by_type', name="by_type"),
    url(r'^job/(?P<job_id>\d+)', 'job', name="job"),
    url(r'^preview', 'preview', name="preview"),
    url(r'^publish', 'publish', name="publish"),
    url(r'^new', 'new', name="new"),  
)

