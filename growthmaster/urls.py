from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('services/', include('services.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('contact/', include('contacts.urls')),
    path('subscribers/', include('subscribers.urls')),
    path('accounts/', include('accounts.urls')),
    path('manage/', include('manage_portal.urls')),
    path('email/', include('email_broadcast.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
