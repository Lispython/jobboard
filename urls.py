# -*- coding: utf-8 -*-

from os.path import join


from django.contrib import admin
from django.conf.urls.defaults import *
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^flycenter/', include(admin.site.urls)),
    url(r'^feedback/', include('feedback.urls')),
    url(r'^captcha/(?P<code>[\da-f]{32})/$', 'supercaptcha.draw'), 
    url(r'^', include('board.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': join(settings.PROJECT_ROOT, 'media')}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': join(settings.PROJECT_ROOT, 'static')}),
    )

handler404 = 'lib.j2lib.defaults.page_not_found'
handler500 = 'lib.j2lib.defaults.server_error'

