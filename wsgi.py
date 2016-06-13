#!/usr/bin/env python
# coding: utf-8
 
import os
import sys
 
# 将系统的编码设置为UTF8
#reload(sys)
#sys.setdefaultencoding('utf8')
 
#注意："mysite.settings" 和项目文件夹对应。
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_puppet_salt_web.settings")
 
#from django.core.handlers.wsgi import WSGIHandler
#application = WSGIHandler()
 
# 上面两行测试不对，然后从stackflow上面看到了下面两行，测试ok
from django.core.wsgi import get_wsgi_application 
application = get_wsgi_application()
