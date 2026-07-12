"""Shared helpers for sending emails that match the website's branding."""
from django.conf import settings
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils import timezone

from .models import SiteSettings


def base_url():
    return getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000').rstrip('/')


def render_branded_email(content_html, *, subject='', preview_text='', unsub_url='', pixel=''):
    """Wrap arbitrary HTML content in the branded GrowthMaster email layout.

    `unsub_url` and `pixel` are optional — omit them for transactional emails
    (e.g. direct replies) that should not carry marketing tracking/unsubscribe.
    """
    site = SiteSettings.load()
    logo_url = base_url() + (site.logo.url if site.logo else static('images/growthmaster-icon.png'))
    return render_to_string('email/base_email.html', {
        'content': content_html,
        'subject': subject,
        'preview_text': preview_text,
        'site': site,
        'logo_url': logo_url,
        'year': timezone.now().year,
        'unsub_url': unsub_url,
        'pixel': pixel,
    })
