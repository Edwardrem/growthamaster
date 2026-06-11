from django.contrib import admin
from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'order')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'short_desc')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('category', 'order')
