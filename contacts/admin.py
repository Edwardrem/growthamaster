from django.contrib import admin
from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'service', 'status', 'created_at')
    list_filter   = ('status', 'service')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('ip_address', 'created_at')
    ordering = ('-created_at',)
