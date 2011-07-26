# -*- coding: utf-8 -*-

import re

from django.forms.fields import RegexField
from django.utils.translation import ugettext_lazy as _
from django.db.models import OneToOneField, CharField
from django.db.models.fields.related import SingleRelatedObjectDescriptor

slug_re = re.compile(ur'^[-,\' \+\w_]+$', re.U)


class SlugFieldForm(RegexField):
    default_error_messages = {
        'invalid': _(u"Enter a valid 'slug' consisting of letters, numbers,"
                     u" underscores or hyphens."),
    }

    def __init__(self, *args, **kwargs):
        super(SlugFieldForm, self).__init__(slug_re, *args, **kwargs)


class SlugField(CharField):
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 150)
        # Set db_index=True unless it's been set manually.
        if 'db_index' not in kwargs:
            kwargs['db_index'] = True
        super(SlugField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "SlugField"

    def formfield(self, **kwargs):
        defaults = {'form_class': SlugFieldForm}
        defaults.update(kwargs)
        return super(SlugField, self).formfield(**defaults)


class AutoSingleRelatedObjectDescriptor(SingleRelatedObjectDescriptor):

    def __get__(self, instance, instance_type=None):
        try:
            return super(AutoSingleRelatedObjectDescriptor, self).__get__(instance, instance_type)
        except self.related.model.DoesNotExist:
            obj = self.related.model(**{self.related.field.name: instance})
            obj.save()
            return obj


class AutoOneToOneField(OneToOneField):
    '''
    OneToOneField creates related object on first call if it doesnt exists yet.
    Use it instead of original OneToOne field.

    example:

        class MyProfile(models.Model):
            user = AutoOneToOneField(User, primary_key=True)
            home_page = models.URLField(max_length=255)
            icq = models.CharField(max_length=255)
    '''
    
    def contribute_to_related_class(self, cls, related):
        setattr(cls, related.get_accessor_name(),
                AutoSingleRelatedObjectDescriptor(related))
