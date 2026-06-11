from django.db import models


class Enquiry(models.Model):
    class Status(models.TextChoices):
        NEW      = 'new',      'New'
        READ     = 'read',     'Read'
        REPLIED  = 'replied',  'Replied'
        ARCHIVED = 'archived', 'Archived'

    name       = models.CharField(max_length=100)
    email      = models.EmailField()
    phone      = models.CharField(max_length=30, blank=True)
    service    = models.ForeignKey('services.Service', null=True, blank=True,
                     on_delete=models.SET_NULL, related_name='enquiries')
    message    = models.TextField()
    status     = models.CharField(max_length=10, choices=Status.choices, default=Status.NEW)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Enquiries'

    def __str__(self):
        return f'{self.name} — {self.email} ({self.created_at.date()})'
