from django.contrib import admin
from .models import PortfolioItem


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display  = ('title', 'media_type', 'category', 'is_featured', 'is_active', 'order')
    list_filter   = ('media_type', 'category', 'is_featured', 'is_active')
    search_fields = ('title', 'description', 'client_name')
    ordering      = ('order', '-created_at')
    list_editable = ('is_active', 'is_featured', 'order')
