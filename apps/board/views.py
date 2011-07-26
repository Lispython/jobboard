# -*- coding: utf-8 -*-

import datetime
import uuid

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from supercaptcha.forms import CaptchaForm

from forms import PostForm
from lib.common import mongo
from lib.j2lib.decorators import render_to


@render_to('index.html')
def index(request):
    return {
        }


@render_to('new.html')
def publish(request):
    token = request.POST.get('token', None)
    if not token or request.method == "GET":
        return HttpResponseRedirect(reverse('new'))
    if request.method == "POST":
        captcha_form = CaptchaForm(request.POST)
        if captcha_form.validate():
            job = dict(mongo.previews.find_one({'token': token}))
            job_id = mongo.jobs.find().count() + 1
            job['job_id'] = job_id
            mongo.jobs.insert(job)
            mongo.previews.remove({'token': token})
            return HttpResponseRedirect(reverse('job', args=[job_id]))
        else:
            return HttpResponseRedirect("%s?token=%s" % (reverse('preview'), token))
    return HttpResponseRedirect(reverse('new'))


@render_to('preview.html')
def preview(request):
    token = request.GET.get('token', None)
    if token:
        job = mongo.previews.find_one({'token': token})
        if not job:
            return HttpResponseRedirect(reverse('new'))
    else:
        return HttpResponseRedirect(reverse('new'))
    return {
        'token': token,
        'job': dict(job),
        'captcha_form': CaptchaForm()}


@render_to('new.html')
def new(request):
    from board.utils import obj
    token = request.POST.get('token', None) or request.GET.get('token', None)
    old = dict(mongo.previews.find_one({'token': token})) if token else {}
    form = PostForm(request.POST, obj(old))
    if request.method == "POST" and form.validate():
        token = request.POST.get('token', token)
        job = {"title": form.title.data,
               "job_type": form.job_type.data,
               "date": datetime.datetime.now(),
               "description": form.description.data,
               "how_apply": form.how_apply.data,
               "email": form.email.data,
               "location": form.location.data,
               "url": form.url.data,
               "logo_url": form.logo_url.data,
               "company": form.name.data,
               "category": form.category.data,
               "token": token or uuid.uuid4().hex}
        if token:
            mongo.previews.update({'token': token}, job)
        else:
            mongo.previews.insert(job)
            if 'jobs' not in request.session:
                request.session['jobs'] = []
            request.session['jobs'].append(job['token'])
        return HttpResponseRedirect("%s?token=%s" % (reverse('preview'), job['token']))
    return {
        'form': form,
        'token': token}


@render_to('category.html')
def category(request, cat_id):
    jobs = mongo.jobs.find_one({'category': cat_id})
    return {
        'category': cat_id,
        'jobs': jobs}

@render_to('by_type.html')
def by_type(request, type_id):
    jobs = mongo.jobs.find_one({'job_type': type_id})
    return {
        'type': type_id,
        'jobs': jobs}



@render_to('job.html')
def job(request, job_id):
    job = mongo.jobs.find_one({u'job_id': int(job_id)})
    if not job:
        raise Http404
    return {
        'job': dict(job)}
