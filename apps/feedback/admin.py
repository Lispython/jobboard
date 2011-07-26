# -*- coding: utf-8 -*-

from django.contrib import admin

from models import *


class FeedbackAdmin(admin.ModelAdmin):
    """Feedback admin class"""
    list_display = ('id', 'message', 'email', 'type', 'status')

admin.site.register(Feedback, FeedbackAdmin)
