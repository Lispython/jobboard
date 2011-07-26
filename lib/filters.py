# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.template.defaultfilters import date
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from lib.markups import markup
from lib.utils import sanitize_html


def markdown(value, ext=[]):
    """
    Runs Markdown over a given value, optionally using various
    extensions python-markdown2 supports.

    Syntax::

        {{ value|markdown(['extension1_name','extension2_name']) }}

    To enable safe mode, which strips raw HTML and only returns HTML
    generated by actual Markdown syntax, pass "safe" as the first
    extension in the list.

    If the version of Markdown in use does not support extensions,
    they will be silently ignored.

    """
    try:
        import markdown2
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError, "Error in {% markdown %} filter: The Python markdown2 library isn't installed."
        return sanitize_html(force_unicode(value))
    else:
        if len(ext) > 0 and ext[0] == "safe":
            ext = ext[1:]
            safe_mode = True
        else:
            safe_mode = False
        return mark_safe(markdown2.markdown(sanitize_html(force_unicode(value)), extras=ext, safe_mode=safe_mode))

filters = {
    'markdown': markdown,
    'markup': markup,
    'force_unicode': force_unicode,
    'date': date}
