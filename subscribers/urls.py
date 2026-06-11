from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/<uuid:token>/', views.UnsubscribeView.as_view(), name='unsubscribe'),
]
