from django.db import models


class PortfolioItem(models.Model):
    class MediaType(models.TextChoices):
        VIDEO  = 'video',  'Video'
        PHOTO  = 'photo',  'Photo'
        SOCIAL = 'social', 'Social Media'

    class Category(models.TextChoices):
        STRATEGY = 'strategy', 'Strategy'
        PROJECTS = 'projects', 'Projects'
        RESEARCH = 'research', 'Research'
        EVENTS   = 'events',   'Events'
        GENERAL  = 'general',  'General'

    title        = models.CharField(max_length=150)
    media_type   = models.CharField(max_length=10, choices=MediaType.choices)
    category     = models.CharField(max_length=20, choices=Category.choices, default=Category.GENERAL)
    description  = models.TextField(blank=True)
    thumbnail    = models.ImageField(upload_to='portfolio/thumbs/', blank=True)
    media_url    = models.URLField(blank=True,
                       help_text='YouTube/Vimeo URL for videos; social post URL for embeds')
    embed_code   = models.TextField(blank=True,
                       help_text='Raw embed code for social media posts (Instagram, LinkedIn, etc.)')
    media_file   = models.FileField(upload_to='portfolio/files/', blank=True,
                       help_text='Upload a self-hosted MP4 or full-size photo')
    alt_text     = models.CharField(max_length=200, blank=True)
    caption      = models.CharField(max_length=300, blank=True)
    client_name  = models.CharField(max_length=100, blank=True)
    project_date = models.DateField(null=True, blank=True)
    is_featured  = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    order        = models.PositiveSmallIntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_embed_url(self):
        url = self.media_url
        if 'youtube.com/watch' in url:
            vid = url.split('v=')[-1].split('&')[0]
            return f'https://www.youtube.com/embed/{vid}'
        if 'youtu.be/' in url:
            vid = url.split('youtu.be/')[-1].split('?')[0]
            return f'https://www.youtube.com/embed/{vid}'
        if 'vimeo.com/' in url:
            vid = url.rstrip('/').split('/')[-1]
            return f'https://player.vimeo.com/video/{vid}'
        return url
