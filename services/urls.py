from django.urls import path
from . import views

urlpatterns = [
    path('', views.ServicesListView.as_view(), name='services_list'),
    path('category/<slug:slug>/', views.CategoryServicesPartial.as_view(), name='services_by_category'),
    path('<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
]
