# -*- coding:utf-8 -*-
from base import *
from mongoengine import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'enginet',                      
        'USER': 'admin',
        'PASSWORD': 'admin4u',
        'HOST': '',                      
        'PORT': '',                      
        'STORAGE_ENGINE': 'INNODB',
    }
}

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DB = 'mazezoom'
MONGO_POOL_AUTH = {
    'user': 'root',
    'passwd': 'admin4u',
}

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = 'afc7c7180c3c43b51b1ebfebae76b5e8'
REDIS_CONF = {
    'host': REDIS_HOST,
    'password': REDIS_PASSWORD,
    'port': REDIS_PORT,
    'db': 0,
}

