# -*- coding:  utf-8 -*-

from django.core.cache import cache
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from supercaptcha import *

from wtforms import Form, widgets, validators
from wtforms.fields import Field, HiddenField

import settings


class CaptchaImageWidget(widgets.TextInput):
    if REFRESH:
        template = HTML_TEMPLATE_WITH_REFRESH
    else:
        template = HTML_TEMPLATE

    def __init__(self, *args, **kwargs):
        super(CaptchaImageWidget, self).__init__(*args, **kwargs)

    def __call__(self, field, **kwargs):
        return self.render(field.name, None)

    def build_attrs(self, extra_attrs=None, **kwargs):
        "Helper function for building an attribute dictionary."
        attrs = dict(**kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs

    def render(self, name, attrs=None):
        code = get_current_code()
        input_attrs = self.build_attrs(attrs, type='text', name=name)
        src = reverse(draw, kwargs={'code': code})
        return mark_safe(self.template % {
            'src': src,
            'input_attrs': flatatt(input_attrs),
            'alt': settings.ALT,
            'width': WIDTH,
            'length': LENGTH,
            'height': HEIGHT, 'rnd': random(),
            'refresh_text': REFRESH_LINK_TEXT})


class CaptchaImageField(Field):
    widget = CaptchaImageWidget()

    def __call__(self, **kwargs):
        return self.widget(self, **kwargs)


class HiddenCodeWidget(widgets.HiddenInput):

    def __call__(self, field, **kwargs):
        value = field._value()
        if value is None:
            empty_current_code()
        if not value:
            value = get_current_code()
            field.data = value
        else:
            set_current_code(value)
        return super(HiddenCodeWidget, self).__call__(field, **kwargs)


class HiddenCodeField(HiddenField):
    widget = HiddenCodeWidget()


class CaptchaForm(Form):
    code = HiddenCodeField(_('Captcha hidden code'),
                           [validators.Length(max=32, min=32,
                                              message=_('Length must have 32 charachters')),
                            validators.Required()])
    img = CaptchaImageField(_('Are you human?'),
                            [validators.Required(),
                             validators.Length(min=settings.LENGTH, max=settings.LENGTH)],
                            description=_('Enter if you are a human and you want to publish job'))

    def validate(self, **kwargs):
        success = super(CaptchaForm, self).validate(**kwargs)
        code = self._fields['code'].data
        text = self._fields['img'].data
        cached_text = cache.get('%s-%s' % (PREFIX, code))
        cache.set('%s-%s' % (PREFIX, code), generate_text(), 600)
        if not cached_text:
            success = False
            self._fields['img'].errors.append(_("The code you entered is wrong."))
        if not text:
            success = False
            self._fields['img'].errors.append(_(u'This field is required.'))
        if text.lower() != cached_text.lower():
            success = False
            self._fields['img'].errors.append(_(u'Internal error.'))
        return success
