from django.db import models


class SiteSettings(models.Model):
    site_name        = models.CharField(max_length=120, default='GrowthMaster Solutions')
    tagline          = models.CharField(max_length=255, blank=True, default='Empowering Business Success')
    whatsapp_number  = models.CharField(max_length=25, blank=True,
                           help_text='E.164 format, e.g. +263771234567')
    contact_email    = models.EmailField(blank=True)
    contact_email_secondary = models.EmailField(blank=True)
    phone            = models.CharField(max_length=60, blank=True)
    physical_address = models.TextField(blank=True)
    facebook_url     = models.URLField(blank=True)
    instagram_url    = models.URLField(blank=True)
    linkedin_url     = models.URLField(blank=True)
    twitter_url      = models.URLField(blank=True)
    hero_heading     = models.CharField(max_length=200, blank=True,
                           default='Empowering Business Success')
    hero_subheading  = models.TextField(blank=True,
                           default='Strategy, Projects, Research & Funding consultancy for SMEs, NGOs and investors across Africa.')
    about_body       = models.TextField(blank=True)
    logo             = models.ImageField(upload_to='site/', blank=True)
    favicon          = models.ImageField(upload_to='site/', blank=True)
    footer_text      = models.CharField(max_length=300, blank=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
