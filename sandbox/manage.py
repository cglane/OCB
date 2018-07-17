#!/usr/bin/env python
import os
import sys
from django.conf import settings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings-dev")
    # if getattr(settings, 'DATABASES')['default']['ENGINE'] != 'django.db.backends.sqlite3':
    #     raise Exception('Wrong Database')
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
