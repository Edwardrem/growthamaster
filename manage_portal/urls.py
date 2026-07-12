from django.urls import path
from . import views

urlpatterns = [
    path('', views.ManageDashboard.as_view(), name='manage_dashboard'),
    path('portfolio/', views.PortfolioManager.as_view(), name='manage_portfolio'),
    path('portfolio/add/', views.PortfolioItemCreate.as_view(), name='manage_portfolio_add'),
    path('portfolio/<int:pk>/edit/', views.PortfolioItemEdit.as_view(), name='manage_portfolio_edit'),
    path('portfolio/<int:pk>/delete/', views.PortfolioItemDelete.as_view(), name='manage_portfolio_delete'),
    path('subscribers/', views.SubscriberManager.as_view(), name='manage_subscribers'),
    path('subscribers/export/', views.SubscriberCSVExport.as_view(), name='manage_subscribers_export'),
    path('subscribers/<int:pk>/toggle/', views.SubscriberToggleActive.as_view(), name='manage_subscriber_toggle'),
    path('email/compose/', views.EmailCompose.as_view(), name='manage_email_compose'),
    path('email/sent/', views.EmailSentLog.as_view(), name='manage_email_sent'),
    path('email/analytics/', views.EmailAnalytics.as_view(), name='manage_email_analytics'),
    path('enquiries/', views.EnquiryManager.as_view(), name='manage_enquiries'),
    path('enquiries/export/', views.EnquiryCSVExport.as_view(), name='manage_enquiries_export'),
    path('enquiries/<int:pk>/', views.EnquiryDetail.as_view(), name='manage_enquiry_detail'),
    path('enquiries/<int:pk>/status/', views.EnquiryStatusUpdate.as_view(), name='manage_enquiry_status'),
    path('enquiries/<int:pk>/reply/', views.EnquiryReply.as_view(), name='manage_enquiry_reply'),
    path('settings/', views.SiteSettingsView.as_view(), name='manage_settings'),
]
