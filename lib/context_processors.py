# -*- coding: utf-8 -*-

import logging
import yaml

from django.conf import settings

from lib.common import c_settings


def settings_vars(request=None):
    r = {
        'settings': c_settings}
    if request:
        r['site'] = request.get_host()
    return r


def config(request=None):
    config_file_path = getattr(settings, 'SITE_CONFIG', None)
    try:
        config_stream = open(config_file_path, 'r')
        config = yaml.safe_load(config_stream.read())
        config_stream.close()
    except Exception, e:
        logging.debug(e)
        return {
            'config': ''}
    return {
        'config': config}
