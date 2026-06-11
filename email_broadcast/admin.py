from django.contrib import admin
from .models import Campaign, CampaignRecipient, CampaignLink


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('subject', 'status', 'recipient_count', 'open_count', 'click_count', 'sent_at')
    list_filter = ('status',)
    readonly_fields = ('sent_at', 'recipient_count', 'open_count', 'click_count', 'created_at')
