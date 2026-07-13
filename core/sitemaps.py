from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from services.models import Service


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return ['home', 'about', 'services_list', 'portfolio', 'contact']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == 'home' else 0.8


class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at


SITEMAPS = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
}
