from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Brand', {'fields': ('site_name', 'tagline', 'logo', 'favicon', 'footer_text')}),
        ('Hero', {'fields': ('hero_heading', 'hero_subheading')}),
        ('About', {'fields': ('about_body',)}),
        ('Contact', {'fields': ('contact_email', 'phone', 'physical_address', 'whatsapp_number')}),
        ('Social Media', {'fields': ('linkedin_url', 'facebook_url', 'instagram_url', 'twitter_url')}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
