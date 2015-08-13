# -*- coding:utf-8 -*-

from position import *
from base import PositionSpider


appname = u'民泰'
subclass = PositionSpider.subclass

with open('result.txt', 'a') as f:
    for cls in subclass.values():
        instance = cls(app_name=appname, has_orm=False, is_accurate=False)
        try:
            result = instance.run()
        except Exception, e:
            print e
        else:
            if result:
                name = instance.name
                domain = instance.domain
                for item in result:
                    url = item[0]
                    title = item[1]
                    f.write('%s\t%s\t%s\t%s\n' % (
                            instance.name.encode('utf-8'),
                            instance.domain.encode('utf-8'),
                            url.encode('utf-8'),
                            title.encode('utf-8'))
                    )
            else:
                    f.write('%s\t%s\n' % (
                        instance.name.encode('utf-8'),
                        instance.domain.encode('utf-8'),
                    ))
            f.flush()
