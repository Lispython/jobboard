# -*- coding:  utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import  HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from feedback.forms import FeedbackForm
from feedback.models import Feedback

from lib.decorators import ajax_request
from lib.j2lib import render_to_response


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            Feedback(email=email, message=message, type="gen", status=1).save()
            return HttpResponseRedirect(reverse('feedback_completed'))
            return render_to_response('feedback_completed.html', {}, request)
    else:
        form = FeedbackForm()

    return render_to_response('feedback.html', {
        'form': form}, request)


@ajax_request
def feedback_ajax(request):
    form = FeedbackForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        Feedback(email=email, message=message, type="gen", status=1).save()
        return {
            'status': 201,
            'message': _('Success! Thanks for taking the time to write.')}
    else:
        return {
            'status': 400,
            'message': _(u"Not valid data")}
