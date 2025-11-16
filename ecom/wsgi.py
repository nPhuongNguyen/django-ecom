"""
WSGI config for ecom project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from apps.logging.sql_logger_setup import setup_sql_logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')

application = get_wsgi_application()
setup_sql_logger()
