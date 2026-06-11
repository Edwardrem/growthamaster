import uuid
from django.conf import settings
from django.db import models


class Campaign(models.Model):
    class Status(models.TextChoices):
        DRAFT   = 'draft',   'Draft'
        SENDING = 'sending', 'Sending'
        SENT    = 'sent',    'Sent'
        FAILED  = 'failed',  'Failed'

    subject          = models.CharField(max_length=200)
    preview_text     = models.CharField(max_length=200, blank=True)
    html_body        = models.TextField()
    text_body        = models.TextField(blank=True)
    status           = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    sent_at          = models.DateTimeField(null=True, blank=True)
    created_by       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                           null=True, blank=True)
    recipient_count  = models.PositiveIntegerField(default=0)
    open_count       = models.PositiveIntegerField(default=0)
    click_count      = models.PositiveIntegerField(default=0)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject

    @property
    def open_rate(self):
        if self.recipient_count:
            return round(self.open_count / self.recipient_count * 100, 1)
        return 0.0

    @property
    def click_rate(self):
        if self.recipient_count:
            return round(self.click_count / self.recipient_count * 100, 1)
        return 0.0


class CampaignRecipient(models.Model):
    campaign     = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='recipients')
    subscriber   = models.ForeignKey('subscribers.Subscriber', on_delete=models.CASCADE)
    email        = models.EmailField()
    pixel_token  = models.UUIDField(default=uuid.uuid4, unique=True)
    opened       = models.BooleanField(default=False)
    opened_at    = models.DateTimeField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.campaign} → {self.email}'


class CampaignLink(models.Model):
    campaign      = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='links')
    original_url  = models.URLField()
    token         = models.UUIDField(default=uuid.uuid4, unique=True)
    click_count   = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.campaign} — {self.original_url[:60]}'
