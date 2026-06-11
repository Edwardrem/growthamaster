from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views import View

from services.models import Service
from .forms import EnquiryForm
from .models import Enquiry


def _get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class ContactView(View):
    template_name = 'contacts/contact.html'

    def get(self, request):
        service_slug = request.GET.get('service')
        initial = {}
        if service_slug:
            svc = Service.objects.filter(slug=service_slug, is_active=True).first()
            if svc:
                initial['service'] = svc
        form = EnquiryForm(initial=initial)
        return render(request, self.template_name, {'form': form})


class ContactSubmitView(View):
    def post(self, request):
        form = EnquiryForm(request.POST)
        is_htmx = request.headers.get('HX-Request')
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.ip_address = _get_client_ip(request)
            enquiry.save()
            _send_notification(enquiry, request)
            if is_htmx:
                return render(request, 'contacts/partials/success.html', {'enquiry': enquiry})
            return render(request, 'contacts/contact.html', {'form': EnquiryForm(), 'submitted': True})
        if is_htmx:
            return render(request, 'contacts/partials/form.html', {'form': form})
        return render(request, 'contacts/contact.html', {'form': form})


def _send_notification(enquiry, request):
    admin_email = getattr(settings, 'ADMIN_EMAIL', '')
    if not admin_email:
        return
    subject = f'New Enquiry from {enquiry.name} — GrowthMaster'
    body = (
        f'New enquiry received on GrowthMaster website.\n\n'
        f'Name:    {enquiry.name}\n'
        f'Email:   {enquiry.email}\n'
        f'Phone:   {enquiry.phone or "—"}\n'
        f'Service: {enquiry.service.name if enquiry.service else "—"}\n\n'
        f'Message:\n{enquiry.message}\n\n'
        f'View in portal: {settings.BASE_URL}/manage/enquiries/'
    )
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [admin_email], fail_silently=True)
    except Exception:
        pass
