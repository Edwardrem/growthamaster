from django.contrib import admin
from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display  = ('email', 'first_name', 'is_active', 'source', 'subscribed_at')
    list_filter   = ('is_active', 'source')
    search_fields = ('email', 'first_name')
    readonly_fields = ('token', 'subscribed_at', 'unsubscribed_at')
    ordering = ('-subscribed_at',)
