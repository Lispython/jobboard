# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from lib.j2lib import direct_to_template


urlpatterns = patterns('feedback.views',
    url(r'^ajax/', 'feedback_ajax', name="feedback_ajax"),
    url(r'^completed/', direct_to_template,
        {'template': 'feedback_completed.html'}, name="feedback_completed"),
    url(r'^', 'feedback', name="feedback"))
