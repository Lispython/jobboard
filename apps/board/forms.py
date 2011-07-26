# -*- coding:  utf-8 -*-

from django.utils.translation import gettext as _

from wtforms import Form, TextField, validators, SelectField, RadioField
from wtforms.widgets import TextArea

from board.settings import cats, job_types


class PostForm(Form):
    title = TextField(_('Job title'), [validators.Length(min=4, max=255),
                                       validators.Required()],
                      description=_(u"Job title help text"))
    description = TextField(_('Job description'), [validators.Length(min=100),
                                                   validators.Required()],
                            widget=TextArea())
    category = SelectField(_('Category'), choices=cats, coerce=int)
    email = TextField(_('Email'), [
        validators.Length(min=6, message=_('Little short for an email address?')),
        validators.Email(message=_('That\'s not a valid email address.')),
        validators.Required()])
    name = TextField(_('Company name'), [validators.Length(min=4, max=255), validators.Required()])
    url = TextField(_('Company url'), [validators.Required(), validators.URL()])
    logo_url = TextField(_('Company logo url'), [validators.URL()])
    location = TextField(_('Job location'), [validators.Length(min=4, max=255),
                                             validators.Required()])
    how_apply = TextField(_('How do people apply for this job?'), [validators.Length(min=4, max=255),
                                                                   validators.Required()],
                          widget=TextArea())
    job_type = RadioField(_('Job type'), [], coerce=int, choices=job_types)
    #captcha = FormField(CaptchaForm)
