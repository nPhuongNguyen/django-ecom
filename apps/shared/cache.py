__all__ = [
    'Caching',
]

import logging

from django.conf import settings
from django.core.cache import caches

logger = logging.getLogger(__name__)


class Caching:
    @classmethod
    def key__user(cls, user_id):
        return 'user_' + str(user_id)

    def __init__(self, alias='default', is_silent: bool = True):
        self.sv = caches[alias]
        self.is_silent = is_silent

    def get(self, key, default=None):
        try:
            return self.sv.get(key, default=default)
        except Exception as err:  # pylint: disable=W0718
            logger.error('[CACHING][GET] Error: %s', str(err))
        return None

    def set(self, key, value, expires=None):
        try:
            if not expires:
                expires = settings.CACHE_EXPIRE_SECONDS

            return self.sv.set(key, value, timeout=expires)
        except Exception as err:  # pylint: disable=W0718
            logger.error('[CACHING][SET] Error: %s', str(err))
        return None

    def delete(self, key):
        try:
            return self.sv.delete(key)
        except Exception as err:  # pylint: disable=W0718
            logger.error('[CACHING][DELETE] Error: %s', str(err))
        return None
