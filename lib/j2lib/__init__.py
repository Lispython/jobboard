# -*- coding: utf-8 -*-

"""
Adds support for Jinja2 to Django.
"""

import traceback
import gettext
import logging
try:
    from cProfile import Profile
except ImportError:
    from profile import Profile

import time
from itertools import chain
from django.conf import settings
from django.http import HttpResponse
from django.utils.importlib import import_module
from django.template import TemplateDoesNotExist, InvalidTemplateLibrary
from django.core.exceptions import ImproperlyConfigured
from django.template.context import get_standard_processors

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from jinja2.defaults import DEFAULT_NAMESPACE

from j2lib.exceptions import (J2libTemplateError, J2libTemplateSyntaxError)


# the environment is unconfigured until the first template is loaded.
_jinja_env = None

libraries = {}


def get_env():
    """Get the Jinja2 env and initialize it if necessary."""
    global _jinja_env
    if _jinja_env is None:
        _jinja_env = create_env()
    return _jinja_env


def create_env():
    """Create a new Jinja2 environment."""
    searchpath = list(settings.TEMPLATE_DIRS)

    env = Environment(loader=FileSystemLoader(searchpath),
                       auto_reload=settings.TEMPLATE_DEBUG,
                       cache_size=getattr(settings, 'JINJA2_CACHE_SIZE', 50),
                       extensions=getattr(settings, 'JINJA2_EXTENSIONS', ()))
    filters = getattr(settings, 'JINJA2_FILTERS', ())
    globals = getattr(settings, 'JINJA2_GLOBALS', ())
    env.filters.update(load_filters(filters))
    env.globals.update(load_globals(globals))

    try:
        translations = gettext.translation(getattr(settings, 'GETTEXT_DOMAIN', 'django'), 
                                           getattr(settings, 'LOCALE_DIR', './locale/ '))
        env.install_gettext_translations(translations)
    except:
        env.install_null_translations()
    return env


def load_filters(filters):
    result = {}
    for m in filters:
        f = __import__(m, fromlist=['filters'])
        result.update(f.filters)
    return result


def load_extensions(extensions):
    """
    Load the extensions from the list and bind it to the environment.
    Returns a dict of instanciated environments.
    """
    result = {}
    for extension in extensions:
        if isinstance(extension, basestring):
            extension = import_string(extension)
        result[extension.identifier] = extension(environment)
    return result


def load_globals(globals, key="globals"):
    result = {}
    for m in globals:
        f = __import__(m, fromlist=[key])
        result.update(f.globals)
    return result


def get_template(template_name, globals=None):
    """Load a template."""
    try:
        return get_env().get_template(template_name, globals=globals)
    except TemplateNotFound, e:
        raise TemplateDoesNotExist(str(e))


def select_template(templates, globals=None):
    """Try to load one of the given templates."""
    env = get_env()
    for template in templates:
        try:
            return env.get_template(template, globals=globals)
        except TemplateNotFound:
            continue
    raise TemplateDoesNotExist(', '.join(templates))


def render_to_string(template_name, context=None, request=None,
                     processors=None):
    """Render a template into a string."""
    context = dict(context or {})
    if request is not None:
        context['request'] = request
        for processor in chain(get_standard_processors(), processors or ()):
            context.update(processor(request))
    return get_template(template_name).render(context)


def render_to_response(template_name, context=None, request=None,
                       processors=None, mimetype=None, response_class=HttpResponse):
    """Render a template into a response object."""
    return response_class(render_to_string(template_name, context, request,
                                         processors), mimetype=mimetype)


def direct_to_template(request, template, extra_context=None, mimetype=None, **kwargs):
    """
    Render a given template with any extra URL parameters in the context as
    ``{{ params }}``.
    """
    if extra_context is None:
        extra_context = {}
    dictionary = {'params': kwargs}
    for key, value in extra_context.items():
        if callable(value):
            dictionary[key] = value()
        else:
            dictionary[key] = value
    return render_to_response(template, request=request,
                              context=dictionary, mimetype=mimetype)
