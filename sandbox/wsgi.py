# isort:skip
import os
import sys
##Need to change path for aws
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ['HTTPS'] = "on"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings-prod")
here = os.path.dirname(__file__)
from django.core.wsgi import get_wsgi_application  # isort:skip

application = get_wsgi_application()
