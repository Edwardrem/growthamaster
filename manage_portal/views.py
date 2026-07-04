import csv
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.core.paginator import Paginator

from contacts.models import Enquiry
from core.models import SiteSettings
from email_broadcast.models import Campaign
from portfolio.models import PortfolioItem
from portfolio.forms import PortfolioItemForm
from subscribers.models import Subscriber
from core.forms import SiteSettingsForm


@method_decorator(login_required, name='dispatch')
class ManageDashboard(View):
    template_name = 'manage_portal/dashboard.html'

    def get(self, request):
        today = timezone.now().date()
        ctx = {
            'total_subscribers': Subscriber.objects.filter(is_active=True).count(),
            'new_enquiries_today': Enquiry.objects.filter(
                created_at__date=today, status=Enquiry.Status.NEW).count(),
            'campaigns_this_month': Campaign.objects.filter(
                sent_at__month=today.month, sent_at__year=today.year).count(),
            'portfolio_items': PortfolioItem.objects.filter(is_active=True).count(),
            'recent_enquiries': Enquiry.objects.select_related('service')[:5],
            'recent_campaigns': Campaign.objects.order_by('-created_at')[:3],
        }
        return render(request, self.template_name, ctx)


@method_decorator(login_required, name='dispatch')
class PortfolioManager(View):
    template_name = 'manage_portal/portfolio_manager.html'

    def get(self, request):
        items = PortfolioItem.objects.all()
        return render(request, self.template_name, {'items': items})


@method_decorator(login_required, name='dispatch')
class PortfolioItemCreate(View):
    template_name = 'manage_portal/portfolio_form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': PortfolioItemForm(), 'action': 'Add'})

    def post(self, request):
        form = PortfolioItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_portfolio')
        return render(request, self.template_name, {'form': form, 'action': 'Add'})


@method_decorator(login_required, name='dispatch')
class PortfolioItemEdit(View):
    template_name = 'manage_portal/portfolio_form.html'

    def get(self, request, pk):
        item = get_object_or_404(PortfolioItem, pk=pk)
        return render(request, self.template_name, {'form': PortfolioItemForm(instance=item), 'item': item, 'action': 'Edit'})

    def post(self, request, pk):
        item = get_object_or_404(PortfolioItem, pk=pk)
        form = PortfolioItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('manage_portfolio')
        return render(request, self.template_name, {'form': form, 'item': item, 'action': 'Edit'})


@method_decorator(login_required, name='dispatch')
class PortfolioItemDelete(View):
    def post(self, request, pk):
        item = get_object_or_404(PortfolioItem, pk=pk)
        item.delete()
        return redirect('manage_portfolio')


@method_decorator(login_required, name='dispatch')
class SubscriberManager(View):
    template_name = 'manage_portal/subscriber_manager.html'

    def get(self, request):
        qs = Subscriber.objects.all()
        q = request.GET.get('q', '')
        status = request.GET.get('status', '')
        if q:
            qs = qs.filter(email__icontains=q) | qs.filter(first_name__icontains=q)
        if status == 'active':
            qs = qs.filter(is_active=True)
        elif status == 'unsubscribed':
            qs = qs.filter(is_active=False)
        paginator = Paginator(qs.order_by('-subscribed_at'), 25)
        page = paginator.get_page(request.GET.get('page'))
        return render(request, self.template_name, {
            'page_obj': page, 'q': q, 'status': status,
            'total_active': Subscriber.objects.filter(is_active=True).count(),
        })


@method_decorator(login_required, name='dispatch')
class SubscriberCSVExport(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'
        writer = csv.writer(response)
        writer.writerow(['Email', 'First Name', 'Active', 'Source', 'Subscribed At', 'Unsubscribed At'])
        for s in Subscriber.objects.order_by('-subscribed_at'):
            writer.writerow([
                s.email, s.first_name, s.is_active, s.source,
                s.subscribed_at.strftime('%Y-%m-%d %H:%M'),
                s.unsubscribed_at.strftime('%Y-%m-%d %H:%M') if s.unsubscribed_at else '',
            ])
        return response


@method_decorator(login_required, name='dispatch')
class SubscriberToggleActive(View):
    def post(self, request, pk):
        sub = get_object_or_404(Subscriber, pk=pk)
        sub.is_active = not sub.is_active
        if not sub.is_active:
            sub.unsubscribed_at = timezone.now()
        sub.save(update_fields=['is_active', 'unsubscribed_at'])
        return render(request, 'manage_portal/partials/subscriber_row.html', {'sub': sub})


@method_decorator(login_required, name='dispatch')
class EmailCompose(View):
    template_name = 'manage_portal/email_compose.html'

    def get(self, request):
        return render(request, self.template_name, {'campaign': None})

    def post(self, request):
        subject  = request.POST.get('subject', '').strip()
        html_body = request.POST.get('html_body', '').strip()
        if not subject or not html_body:
            return render(request, self.template_name, {
                'error': 'Subject and body are required.',
                'subject': subject, 'html_body': html_body,
            })
        campaign = Campaign.objects.create(
            subject=subject,
            html_body=html_body,
            preview_text=request.POST.get('preview_text', ''),
            created_by=request.user,
        )
        from email_broadcast.tasks import send_campaign
        send_campaign(campaign.pk)
        return redirect('manage_email_sent')


@method_decorator(login_required, name='dispatch')
class EmailSentLog(View):
    template_name = 'manage_portal/email_sent_log.html'

    def get(self, request):
        campaigns = Campaign.objects.order_by('-created_at')
        return render(request, self.template_name, {'campaigns': campaigns})


@method_decorator(login_required, name='dispatch')
class EmailAnalytics(View):
    template_name = 'manage_portal/email_analytics.html'

    def get(self, request):
        campaigns = Campaign.objects.filter(status=Campaign.Status.SENT).order_by('-sent_at')
        # Chart data: campaigns over time (oldest -> newest), bar heights as % of scale
        chart_campaigns = list(reversed(campaigns[:12]))
        max_rate = max(
            [c.open_rate for c in chart_campaigns] +
            [c.click_rate for c in chart_campaigns] + [0]
        )
        scale = max(10, -(-int(max_rate) // 10) * 10)  # round up to nearest 10, min 10
        chart_data = [{
            'campaign': c,
            'open_h': round(c.open_rate / scale * 100, 1),
            'click_h': round(c.click_rate / scale * 100, 1),
        } for c in chart_campaigns]
        return render(request, self.template_name, {
            'campaigns': campaigns,
            'chart_data': chart_data,
            'chart_scale': scale,
            'chart_gridlines': [scale, scale * 3 // 4, scale // 2, scale // 4],
        })


@method_decorator(login_required, name='dispatch')
class EnquiryManager(View):
    template_name = 'manage_portal/enquiry_manager.html'

    def get(self, request):
        qs = Enquiry.objects.select_related('service')
        status_filter = request.GET.get('status', '')
        if status_filter:
            qs = qs.filter(status=status_filter)
        paginator = Paginator(qs, 20)
        page = paginator.get_page(request.GET.get('page'))
        return render(request, self.template_name, {
            'page_obj': page,
            'status_filter': status_filter,
            'status_choices': Enquiry.Status.choices,
        })


@method_decorator(login_required, name='dispatch')
class EnquiryCSVExport(View):
    def get(self, request):
        qs = Enquiry.objects.select_related('service').order_by('-created_at')
        status_filter = request.GET.get('status', '')
        if status_filter:
            qs = qs.filter(status=status_filter)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="enquiries.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone', 'Service', 'Status', 'Message', 'Date'])
        for e in qs:
            writer.writerow([
                e.name, e.email, e.phone,
                e.service.name if e.service else '',
                e.get_status_display(), e.message,
                e.created_at.strftime('%Y-%m-%d %H:%M'),
            ])
        return response


@method_decorator(login_required, name='dispatch')
class EnquiryDetail(View):
    template_name = 'manage_portal/enquiry_detail.html'

    def get(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        if enquiry.status == Enquiry.Status.NEW:
            enquiry.status = Enquiry.Status.IN_PROGRESS
            enquiry.save(update_fields=['status'])
        return render(request, self.template_name, {'enquiry': enquiry})


@method_decorator(login_required, name='dispatch')
class EnquiryStatusUpdate(View):
    def post(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Enquiry.Status.choices):
            enquiry.status = new_status
            enquiry.save(update_fields=['status'])
        return render(request, 'manage_portal/partials/enquiry_status_badge.html', {'enquiry': enquiry})


@method_decorator(login_required, name='dispatch')
class SiteSettingsView(View):
    template_name = 'manage_portal/settings.html'

    def get(self, request):
        settings_obj = SiteSettings.load()
        form = SiteSettingsForm(instance=settings_obj)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        settings_obj = SiteSettings.load()
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            cache.delete('site_settings')
            return redirect('manage_settings')
        return render(request, self.template_name, {'form': form})
