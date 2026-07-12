import re
import uuid
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.utils import timezone

from core.emails import render_branded_email
from subscribers.models import Subscriber
from .models import Campaign, CampaignLink, CampaignRecipient

TRANSPARENT_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff'
    b'\x00\x00\x00\x21\xf9\x04\x00\x00\x00\x00\x00\x2c\x00\x00\x00\x00'
    b'\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
)


def _rewrite_links(html, campaign, base_url):
    link_map = {}
    def replace_href(match):
        original = match.group(1)
        if original.startswith('mailto:') or original.startswith('#'):
            return match.group(0)
        if original in link_map:
            cl = link_map[original]
        else:
            cl = CampaignLink.objects.create(campaign=campaign, original_url=original)
            link_map[original] = cl
        tracked = f'{base_url}/email/click/{cl.token}/'
        return f'href="{tracked}"'
    return re.sub(r'href="([^"]+)"', replace_href, html)


def send_campaign(campaign_id):
    try:
        campaign = Campaign.objects.get(pk=campaign_id)
    except Campaign.DoesNotExist:
        return

    campaign.status = Campaign.Status.SENDING
    campaign.save(update_fields=['status'])

    subscribers = list(Subscriber.objects.filter(is_active=True))
    base_url = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000').rstrip('/')

    html_with_links = _rewrite_links(campaign.html_body, campaign, base_url)

    # Wrap the admin's content in the branded website-styled email layout once,
    # using placeholders for the per-recipient pixel and unsubscribe link.
    shell_html = render_branded_email(
        html_with_links,
        subject=campaign.subject,
        preview_text=campaign.preview_text,
        unsub_url='__UNSUB_URL__',
        pixel='__PIXEL__',
    )

    messages = []
    recipients = []
    for sub in subscribers:
        cr = CampaignRecipient(
            campaign=campaign,
            subscriber=sub,
            email=sub.email,
            pixel_token=uuid.uuid4(),
        )
        recipients.append(cr)
        pixel = f'<img src="{base_url}/email/open/{cr.pixel_token}.gif" width="1" height="1" alt="" />'
        unsub_link = f'{base_url}/subscribers/unsubscribe/{sub.token}/'
        personal_html = shell_html.replace('__PIXEL__', pixel).replace('__UNSUB_URL__', unsub_link)
        text_body = campaign.text_body or ''
        msg = EmailMultiAlternatives(
            subject=campaign.subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sub.email],
        )
        msg.attach_alternative(personal_html, 'text/html')
        messages.append(msg)

    CampaignRecipient.objects.bulk_create(recipients)

    try:
        connection = get_connection()
        connection.open()
        connection.send_messages(messages)
        connection.close()
        campaign.status = Campaign.Status.SENT
        campaign.recipient_count = len(subscribers)
        campaign.sent_at = timezone.now()
    except Exception as exc:
        campaign.status = Campaign.Status.FAILED
        campaign.text_body = str(exc)
    finally:
        campaign.save(update_fields=['status', 'recipient_count', 'sent_at', 'text_body'])
