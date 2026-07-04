from django.shortcuts import render
from django.views import View

from .models import PortfolioItem


class PortfolioView(View):
    template_name = 'portfolio/gallery.html'

    def get(self, request):
        items = PortfolioItem.objects.filter(is_active=True)
        return render(request, self.template_name, {
            'items': items,
            'categories': PortfolioItem.Category.choices,
        })


class PortfolioFilterPartial(View):
    def get(self, request):
        qs = PortfolioItem.objects.filter(is_active=True)
        media_type = request.GET.get('type', '')
        category   = request.GET.get('cat', '')
        if media_type in ('video', 'photo', 'social'):
            qs = qs.filter(media_type=media_type)
        if category:
            qs = qs.filter(category=category)
        page = int(request.GET.get('page', 1))
        per_page = 12
        start = (page - 1) * per_page
        total = qs.count()
        items = qs[start:start + per_page]
        return render(request, 'portfolio/partials/filter_results.html', {
            'items': items,
            'has_more': (start + per_page) < total,
            'next_page': page + 1,
            'media_type': media_type,
            'category': category,
        })
