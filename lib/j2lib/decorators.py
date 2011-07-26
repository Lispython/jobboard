# -*- coding: utf-8 -*-

from j2lib import render_to_response

def render_to(template):
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], request)
            elif isinstance(output, dict):
                return render_to_response(template, output, request)
            return output
        return wrapper
    return renderer
