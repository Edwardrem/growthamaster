from django.urls import path
from . import views

urlpatterns = [
    path('open/<uuid:token>.gif', views.PixelTrackerView.as_view(), name='email_open_tracker'),
    path('click/<uuid:token>/', views.LinkTrackerView.as_view(), name='email_link_tracker'),
]
