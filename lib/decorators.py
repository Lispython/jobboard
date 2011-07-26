# -*- coding: utf-8 -*-

import traceback

from django.db.models import signals as signalmodule

from common import JSONResponse


class Signals(object):
    '''
    Convenient wrapper for working with Django's signals (or any other
    implementation using same API).

    Example of usage::


       # connect to registered signal
       @signals.post_save(sender=YourModel)
       def sighandler(instance, **kwargs):
           pass

       # connect to any signal
       signals.register_signal(siginstance, signame) # and then as in example above

       or 
        
       @signals(siginstance, sender=YourModel)
       def sighandler(instance, **kwargs):
           pass

    In any case defined function will remain as is, without any changes.

    (c) 2008 Alexander Solovyov, new BSD License
    '''
    def __init__(self):
        self._signals = {}

        # register all Django's default signals
        for k, v in signalmodule.__dict__.iteritems():
            # that's hardcode, but IMHO it's better than isinstance
            if not k.startswith('__') and k != 'Signal':
                self.register_signal(v, k)

    def __getattr__(self, name):
        return self._connect(self._signals[name])

    def __call__(self, signal, **kwargs):
        def inner(func):
            signal.connect(func, **kwargs)
            return func
        return inner

    def _connect(self, signal):
        def wrapper(**kwargs):
            return self(signal, **kwargs)
        return wrapper

    def register_signal(self, signal, name):
        self._signals[name] = signal

signals = Signals()


def is_authenticated(f):
    def wrapper(request, *args, **kw):
        if(not request.user.is_authenticated()):
            json = {'success': False, 'code':401, 'message':'authentication required'}
            return JSONResponse(json, is_iterable=False)
        return f(request)
    return wrapper


def ajax_request(func):
    """
    If view returned serializable dict, returns JsonResponse with this dict as content.

    example:
        
        @ajax_request
        def my_view(request):
            news = News.objects.all()
            news_titles = [entry.title for entry in news]
            return {'news_titles': news_titles}
    """
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            try:
                response = func(request, *args, **kwargs)
            except Exception, ex:
                response = { 'success': False, 'code':500, 'message': ex}
        else:
            response = {'success': False, 'code': 403, 'message': 'Accepts only POST request'}
        if isinstance(response, dict):
            return JSONResponse(response)
        else:
            return response
    return wrapper
