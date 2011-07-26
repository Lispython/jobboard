# -*- coding: utf-8 -*-

from django.http import HttpResponseNotFound, HttpResponseServerError
from lib.j2lib import render_to_response


def page_not_found(request):
    return render_to_response('404.html', {'request_path': request.path},
                              request, response_class=HttpResponseNotFound)


def server_error(request):
    return render_to_response('500.html', {}, request,
                              response_class=HttpResponseServerError)
