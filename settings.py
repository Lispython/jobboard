# -*- coding: utf-8 -*-

import sys
import os.path
import logging

PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))

def rel(*parts):
    return os.path.join(PROJECT_ROOT, *parts)


sys.path.append(os.path.join(PROJECT_ROOT, 'apps'))
sys.path.append(os.path.join(PROJECT_ROOT, 'lib'))


DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_SRC_ROOT = PROJECT_ROOT


#for OpenID auth
ugettext = lambda s: s

#system will send admins email about error stacktrace if DEBUG=False
ADMINS = (
    ('admin', 'admin@example.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


MONGO_HOST = "localhost"
MONGO_DB = 'jobboard'
MONGO_PORT = 27017

SERVER_EMAIL = ''
DEFAULT_FROM_EMAIL = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = ''
EMAIL_HOST=''
EMAIL_PORT='587'
EMAIL_USE_TLS=True


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'en-En'

SITE_ID = 1


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = rel("media")
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

STATIC_ROOT = rel('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$oo^&kjcbnuierwfhiuu6yigmfregvrebvgrt'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.CacheMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth", 
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "lib.context_processors.settings_vars",
    "lib.context_processors.config", 
)


ROOT_URLCONF = 'urls'

    
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

JINJA2_EXTENSIONS = (
    'jinja2.ext.do',
    'jinja2.ext.i18n',
    'lib.j2lib.ext.url',
    'lib.j2lib.ext.media',
    'lib.j2lib.ext.with_',
    'lib.j2lib.ext.spaceless'
)

JINJA2_FILTERS = (
    'lib.j2lib.filters', 
    'lib.filters',
    'apps.board.filters'
)

JINJA2_GLOBALS = (
    'lib.j2lib.globals',
    'board.globals'
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.redirects',
    'django.contrib.sites', 
    'j2lib',
    'board', 
    'memcache_status',
    'feedback',
    'supercaptcha',
)

LOGIN_REDIRECT_URL = "/"

try:
    from local_settings import *
except ImportError, e:
    import os, warnings
    warnings.warn("Unable import local settings [%s]: %s" % (type(e),  e))
    sys.exit(1)
    logging.debug(e)


SESSION_ENGINE = 'lib.mongo_session_engine'

SITE_CONFIG =  rel('config')
    
if DEBUG:
    INTERNAL_IPS =  ('127.0.0.1', )
    DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
    MIDDLEWARE_CLASSES +=  ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar', )
    DEBUG_TOOLBAR_CONFIG =  {
    'INTERCEPT_REDIRECTS': False
    }

    LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d {{ %(message)s }}'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'full_verbose': {
            'format': 'level: %(levelname)s\n\
            time: %(asctime)s\n\
            mudule: %(module)s [ %(pathname)s]\n \
            line: [%(lineno)d]\n\
            process: %(process)d %(processName)s\n\
            thread: %(thread)d %(threadName)s\n\
            {{ %(message)s }}\n\
            ------------------------------------------------------------------- \n\n'
            }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'full_console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file':{
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'formatter': 'verbose', 
            'filename': rel('debug.log')
        },
        'queries_file':{
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'formatter': 'verbose', 
            'filename': rel('debug_queries.log')

        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'INFO',
            },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR'
        },
        'custom': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'south': {
            'handlers':['queries_file'],
            'level':'DEBUG',
            }
    }
}
else:
    LOGGING =  {
        'version': 1,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d {{ %(message)s }}'
                },
            'simple': {
                'format': '%(levelname)s %(message)s'
                },
            },
        'handlers': {
            'sentry': {
                'class': 'sentry.client.handlers.SentryHandler',
                'level': 'INFO'
                }, 
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True,
                },
            'console': {
                'class':'logging.StreamHandler',
                'level': 'DEBUG',
                },
            'file':{
                'level':'DEBUG',
                'class':'logging.FileHandler',
                'formatter': 'verbose',
                'filename': rel('debug.log')
                }
            },
        'loggers': {
            'sentry.errors': {
                'handlers': ['mail_admins'],
                'level': 'DEBUG',             
                }, 
            'south': {
                'handlers':['file'],
                'level':'DEBUG',
                }
            }
        }
