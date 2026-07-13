from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.generic import TemplateView
from . import views
from .sitemaps import SITEMAPS

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('seed/', views.seed_users, name='seed'),
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain'), name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='sitemap'),
]
