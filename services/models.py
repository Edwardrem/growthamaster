from django.db import models
from django.urls import reverse


class ServiceCategory(models.Model):
    name       = models.CharField(max_length=100)
    slug       = models.SlugField(unique=True)
    order      = models.PositiveSmallIntegerField(default=0)
    icon_class = models.CharField(max_length=60, blank=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return self.name


class Service(models.Model):
    category          = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE,
                            related_name='services')
    name              = models.CharField(max_length=150)
    slug              = models.SlugField(unique=True)
    short_desc        = models.CharField(max_length=300)
    body              = models.TextField()
    key_deliverables  = models.TextField(blank=True,
                            help_text='One deliverable per line — rendered as bullet list')
    cta_label         = models.CharField(max_length=60, default='Enquire Now')
    featured_image    = models.ImageField(upload_to='services/', blank=True)
    is_active         = models.BooleanField(default=True)
    order             = models.PositiveSmallIntegerField(default=0)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})

    def deliverables_list(self):
        return [d.strip() for d in self.key_deliverables.splitlines() if d.strip()]
