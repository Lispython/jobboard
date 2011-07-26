# -*- coding: utf-8 -*-
"""
    jinja2.exceptions
    ~~~~~~~~~~~~~~~~~

    Jinja exceptions.

    :copyright: (c) 2009 by the Jinja Team.
    :license: BSD, see LICENSE for more details.
"""
from jinja2.exceptions import (TemplateError, FilterArgumentError, SecurityError,
                               TemplateAssertionError, TemplateError,
                               TemplateNotFound, TemplateRuntimeError,
                               TemplateSyntaxError, UndefinedError)

class J2libTemplateError(TemplateError):
    """Baseclass for all template errors."""


class J2libTemplateSyntaxError(TemplateSyntaxError):
    """Raised to tell the user that there is a problem with the template."""
