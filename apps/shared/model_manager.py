__all__ = [
    'BaseManager',
]

import hashlib

from django.conf import settings
from django.db import models

from .cache import Caching


class BaseEntryQuerySet(models.query.QuerySet):
    @classmethod
    def hashed_key(cls, txt: str) -> str:
        return hashlib.md5(txt.encode('utf-8')).hexdigest()

    @classmethod
    def flat_filter(cls, filter_data: dict):
        if 'id' in filter_data:
            filter_data['pk'] = filter_data['id']
            del filter_data['id']
        return "&".join(f"{str(k)}={str(v)}" for k, v in sorted(filter_data.items()))

    def _get_deleted_filter(self, is_deleted):
        deleted_filter = {}
        if hasattr(self.model, 'is_deleted') and isinstance(is_deleted, bool):
            deleted_filter = {'is_deleted': is_deleted}
        return deleted_filter

    def _get_model_db_table(self) -> str:
        if self.model and hasattr(self.model, '_meta'):
            return getattr(self.model._meta, 'db_table', '')
        return ''

    def _get_cache_key(self, *args, **kwargs):
        db_table = self._get_model_db_table()
        filter_str = str(self.query)
        argument_data = str(args) + str(kwargs)
        return f'{db_table}:{self.hashed_key(txt=filter_str + argument_data)}'

    def filter(
            self,
            *args,
            is_deleted: bool = False,
            has_cached: bool = False, force_cache: bool = False,
            **kwargs,
    ):
        cache_key = None
        result = None
        cache_cls = Caching()

        # check field is_deleted before force filter
        deleted_filter = self._get_deleted_filter(is_deleted)
        filter_kwargs = {**deleted_filter, **kwargs}

        if force_cache is False and has_cached is True:
            cache_key = self._get_cache_key(*args, is_deleted=is_deleted, **kwargs)
            result = cache_cls.get(key=cache_key, default=None)

        if not result:
            result = super().filter(*args, **filter_kwargs)
            if has_cached is True:
                cache_cls.set(key=cache_key, value=result, expires=settings.CACHE_EXPIRE_SECONDS)
        return result

    def get(
            self,
            *args,
            is_deleted: bool = None,
            has_cached: bool = False, force_cache: bool = False,
            **kwargs,
    ):
        """
        Function call from objects with advance option
        Args:
            is_deleted: (bool, default: None) Filter soft delete with
                * None: skip
                * Bool: filter by value
            has_cached: (default: False) Auto set cache after got data + support check
                cache data before force db
            force_cache: (default: False) Skip check cache data
            **kwargs: dict[str, any] Filter data

        Returns:
            QuerySet
        """
        result = None
        cache_cls = Caching()
        cache_key = None

        # check field is_deleted before force filter
        deleted_filter = self._get_deleted_filter(is_deleted)
        filter_kwargs = {**deleted_filter, **kwargs}

        if force_cache is False and has_cached is True:
            cache_key = self._get_cache_key(*args, is_deleted=is_deleted, **kwargs)
            result = cache_cls.get(key=cache_key, default=None)

        if not result:
            result = super().get(*args, **filter_kwargs)
            if has_cached is True and cache_key:
                cache_cls.set(key=cache_key, value=result, expires=settings.CACHE_EXPIRE_SECONDS)
        return result

    def invalid_cache(self, *args, is_deleted: bool = None, **kwargs):  # pylint: disable=W0613
        cache_key = self._get_cache_key(*args, is_deleted=is_deleted, **kwargs)
        return Caching().delete(key=cache_key)


class BaseManager(models.Manager):
    """
    The class is custom manager that support maintain system
    """

    def get_queryset(self) -> BaseEntryQuerySet:
        """
        Override default is models.query.QuerySet to EntryQuery.
        It supports some method such as: cache, filter_current
        Returns:
            Customize Queryset
        """
        return BaseEntryQuerySet(self.model, using=self._db)

    def invalid_cache(self, *args, is_deleted: bool = None, **kwargs):
        """
        Delegate invalid_cache to BaseEntryQuerySet.
        """
        return self.get_queryset().invalid_cache(*args, is_deleted=is_deleted, **kwargs)
