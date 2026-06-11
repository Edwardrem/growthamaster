import uuid
from django.db import models
from django.utils import timezone


class Subscriber(models.Model):
    email           = models.EmailField(unique=True)
    first_name      = models.CharField(max_length=60, blank=True)
    is_active       = models.BooleanField(default=True)
    token           = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,
                          help_text='Used in unsubscribe links — never expose publicly')
    source          = models.CharField(max_length=60, blank=True,
                          help_text="e.g. 'footer_form', 'contact_page'")
    subscribed_at   = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return f'{self.first_name} <{self.email}>' if self.first_name else self.email

    def unsubscribe(self):
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save(update_fields=['is_active', 'unsubscribed_at'])
