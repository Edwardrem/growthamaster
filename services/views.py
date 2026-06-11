from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from .models import ServiceCategory, Service


class ServicesListView(View):
    template_name = 'services/list.html'

    def get(self, request):
        categories = ServiceCategory.objects.prefetch_related('services').order_by('order')
        active_slug = request.GET.get('cat', None)
        active_cat = None
        if active_slug:
            active_cat = categories.filter(slug=active_slug).first()
        if not active_cat and categories.exists():
            active_cat = categories.first()
        return render(request, self.template_name, {
            'categories': categories,
            'active_cat': active_cat,
        })


class CategoryServicesPartial(View):
    def get(self, request, slug):
        category = get_object_or_404(ServiceCategory, slug=slug)
        services = category.services.filter(is_active=True)
        return render(request, 'services/partials/category_tab.html', {
            'category': category,
            'services': services,
        })


class ServiceDetailView(View):
    template_name = 'services/detail.html'

    def get(self, request, slug):
        service = get_object_or_404(Service, slug=slug, is_active=True)
        related = Service.objects.filter(
            category=service.category, is_active=True
        ).exclude(pk=service.pk)[:4]
        return render(request, self.template_name, {
            'service': service,
            'related': related,
        })
