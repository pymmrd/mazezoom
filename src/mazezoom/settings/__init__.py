# -*- coding:utf-8 -*-

from production import *

try:
    from development import *
except ImportError:
    pass


MONGO_CLIENT = connect(MONGO_DB, host=MONGO_HOST, port=MONGO_PORT)
if MONGO_POOL_AUTH:
    MONGO_CLIENT.admin.authenticate(
        MONGO_POOL_AUTH['user'],
        MONGO_POOL_AUTH['passwd']
    )
