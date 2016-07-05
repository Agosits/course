import sys
import os


sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'course.settings'

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

import django
django.setup()


