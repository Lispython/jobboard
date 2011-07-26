# -*- coding: utf-8 -*-

DEBUG = True
PRODUCTION = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (

   ('Admin', 'admin@example.com'),

)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': 'jobboard.db',
		'USER': 'alex',
		'PASSWORD': 'password',
		},
}

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
MONGO_DB = 'jobboard'

SERVER_EMAIL = 'robot@example.com'
DEFAULT_FROM_EMAIL = 'robot@example.com'
EMAIL_HOST_USER = 'robot@example.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_SUBJECT_PREFIX = 'example.com'
EMAIL_HOST='smtp.yandex.ru'

EMAIL_PORT=587
EMAIL_USE_TLS=True


# Make this unique, and don't share it with anybody.
SECRET_KEY = '$oo^&_m&qwbib=(_4m_n*zn-d=g#s0he5fx9xonnym#8p6yigm'

CACHES = {
  'default': {
      'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
      'LOCATION': ['127.0.0.1:11211','127.0.0.1:11211','127.0.0.1:11213',]
   },
  'dummy': {
      'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
      
   },
  'database_cache': {
      'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
      'LOCATION': 'my_cache_table'
   },
}
