# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.encoding import  force_unicode

from utils import sanitize_html


MARKDOWN = (1, 'markdown')
TEXTILE = (2, 'textile')
#REST = (3, 'restructuredtext')
HTML = (4, 'html')
PLAINTEXT = (5, 'plaintext')
MARKUP_CHOICES = {
    'markdown': MARKDOWN,
    'textile': TEXTILE,
#    'restructuredtext': REST,
    'plaintext': PLAINTEXT,
    'html': HTML}

MARKUPS = {
    1: MARKDOWN,
    2: TEXTILE,
    4: HTML,
    5: PLAINTEXT}

DEFAULT_MARKUP = getattr(settings, 'DEFAULT_MARKUP', HTML)


def get_name_by_id(markup_id):
    return MARKUPS.get(int(markup_id), None)[1]


def markup(value, mtype=1):
    try:
        from django.utils.html import escape
        if mtype == MARKDOWN[0]:
            try:
                import markdown2
            except ImportError:
                try:
                    from django.contrib.markup.templatetags.markup import markdown
                except ImportError:
                    return sanitize_html(force_unicode(value))
                return mark_safe(sanitize_html(markdown(force_unicode(value))))
            else:
                safe_mode = False
                return mark_safe(sanitize_html(markdown2.markdown(force_unicode(value),
                                                                  safe_mode=safe_mode)))
        elif mtype == TEXTILE[0]:
            from django.contrib.markup.templatetags.markup import textile
            return textile(force_unicode(value))
        ## elif mtype == REST[0]:
        ##     from django.contrib.markup.templatetags.markup import restructuredtext
        ##     return restructuredtext(value)
        elif mtype == HTML[0]:
            return mark_safe(sanitize_html(force_unicode(value)))
        elif mtype == PLAINTEXT[0]:
            return escape(force_unicode(value))
        else:
            return markup(value, DEFAULT_MARKUP[0])
    except ImportError:
        # Not marking safe, in case tag fails and users input malicious code.
        return force_unicode(value)
