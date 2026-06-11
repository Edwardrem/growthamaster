from django.urls import path
from . import views

urlpatterns = [
    path('', views.PortfolioView.as_view(), name='portfolio'),
    path('filter/', views.PortfolioFilterPartial.as_view(), name='portfolio_filter'),
]
