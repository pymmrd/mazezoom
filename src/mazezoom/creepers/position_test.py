# -*- coding:utf-8 -*-

from position import *
from base import PositionSpider


appname = u'民泰'
subclass = PositionSpider.subclass

with open('result.txt', 'a') as f:
    for cls in subclass.values():
        instance = cls(app_name=appname, has_orm=False, is_accurate=False)
        try:
            result =  instance.run()
        except Exception, e:
            print e
        else:
            if result:
                for item in result:
                    url = item[0]
                    title = item[1]
                    f.write('%s\t%s\n' % (url.encode('utf-8'), title.encode('utf-8'))) 
                    f.flush()
