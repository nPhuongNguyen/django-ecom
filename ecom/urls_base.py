from django.conf import settings
from django.urls import include, path


def generate_full_prefix_url():
    if settings.PREFIX_URL and settings.API_VERSION:
        return f"{settings.PREFIX_URL.strip('/')}/{settings.API_VERSION.strip('/')}/"
    elif settings.PREFIX_URL:
        return f"{settings.PREFIX_URL.strip('/')}/"
    elif settings.API_VERSION:
        return f"{settings.API_VERSION.strip('/')}/"
    return ''
urlpatterns = [
    path(generate_full_prefix_url(), include('ecom.urls')),
]