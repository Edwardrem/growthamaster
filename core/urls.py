from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain'), name='robots'),
]
