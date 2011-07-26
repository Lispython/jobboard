# -*- coding: utf-8 -*-

from random import choice

from lib.common import mongo
from lib.context_processors import config

from settings import cats, jobs_list, cats_list


def get_by_category(cat_id, limit=0):
    query = {'category': int(cat_id)}
    r = list(mongo.jobs.find(query).limit(int(limit)))
    return sorted(r, key=lambda item: item[u'date'], reverse=True)


def get_job_type(type_id):
    return jobs_list[int(type_id)]


def get_category_name(cat_id):
    return cats_list[int(cat_id)]


def get_categories():
    return cats


def get_tagline():
    return choice(config()['config']['taglines'])


globals = {
    'get_job_type': get_job_type,
    'get_tagline': get_tagline,
    'get_by_category': get_by_category,
    'get_category_name': get_category_name,
    'get_categories': get_categories}
