# -*- coding:utf-8 -*-
from base import *
from mongoengine import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'enginet',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'admin',
        'PASSWORD': 'admin4Mazezoom',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
        'STORAGE_ENGINE': 'INNODB',
    }
}


MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DB = 'mazezoom'
MONGO_POOL_AUTH = {
}
