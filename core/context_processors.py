from django.core.cache import cache
from core.models import SiteSettings


def site_settings(request):
    obj = cache.get('site_settings')
    if obj is None:
        obj = SiteSettings.load()
        cache.set('site_settings', obj, 300)
    return {'site_settings': obj}
