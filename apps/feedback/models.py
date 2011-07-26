# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


TYPE_CHOICES = (
    ('gen', 'General enquiry'),
    ('bug', 'Bug report'),
    ('sug', 'Suggestion'))

STATUS_CHOICES = (
    (1, _(u'Новая задача')),
    (2, _(u'Задача принята на выполнение')),
    (3, _(u'Задача выполнена')))


class Feedback(models.Model):
    ## username = models.CharField(_('username'), max_length=30, unique=False,
    ##                             help_text=u"Необязательно. Используется для обращение по почте.")
    added = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(_('e-mail address'), null=True, blank=True,
                              help_text=_(u"Your e-mail address (optional):"))
    #title = models.CharField(_('title'), max_length=200, help_text=u"Необязательно")
    message = models.TextField(_('message'),
                               help_text=_(u"Send us suggestions, bug reports, love letters, etc."))
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    status = models.IntegerField(choices=STATUS_CHOICES)
