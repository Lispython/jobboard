# -*_ coding: utf-8 -*-

from django.conf import settings
from django.core.serializers import serialize
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.encoding import force_unicode 
from django.utils.functional import Promise
from django.views.debug import get_safe_settings

from pymongo import Connection


mongo_host = getattr(settings, "MONGO_HOST", 'localhost')
mongo_port = getattr(settings, "MONGO_PORT", 27017)
mongo_db = getattr(settings, "MONGO_DB", None)


mongo = Connection(mongo_host, mongo_port)[mongo_db]



class LazyEncoder(simplejson.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj


class JSONResponse(HttpResponse):
    """
    A simple subclass of ``HttpResponse`` which makes serializing to JSON easy.
    """

    def __init__(self, object):
        content = simplejson.dumps(object, cls=LazyEncoder)
        super(JSONResponse, self).__init__(content, mimetype='application/json')


class XMLResponse(HttpResponse):
    """
    A simple subclass of ``HttpResponse`` which makes serializing to XML easy.
    """
    
    def __init__(self, object, is_iterable = True):
        if is_iterable:
            content = serialize('xml', object)
        else:
            content = object
        super(XMLResponse, self).__init__(content, mimetype='application/xml')


class SafeSettings:
    def __init__(self):
        self._settings = None
    
    def __getattr__(self, name):
        if self._settings is None:
            self._settings = get_safe_settings()
        name = name.upper()
        try:
            return self._settings[name]
        except KeyError:
            raise AttributeError


c_settings = SafeSettings()



