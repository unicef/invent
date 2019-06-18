from django.conf import settings
from django.core.cache import cache
from django.utils.translation import get_language


def cache_structure(fn):
    def wrapper(*args, **kwargs):
        cache_key = 'project-structure-data-{}'.format(get_language())
        data = cache.get(cache_key)
        if not data:
            data = fn(*args, **kwargs)
            cache.set(cache_key, data)
        return data

    return wrapper


class InvalidateCacheMixin:
    def save(self, *args, **kwargs):
        for language in settings.LANGUAGES:
            cache_key = 'project-structure-data-{}'.format(language[0])
            cache.delete(cache_key)
        return super().save(*args, **kwargs)
