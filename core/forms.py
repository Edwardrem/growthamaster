from django import forms
from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        exclude = ('updated_at',)
        widgets = {
            'site_name':        forms.TextInput(attrs={'class': 'input-field'}),
            'tagline':          forms.TextInput(attrs={'class': 'input-field'}),
            'whatsapp_number':  forms.TextInput(attrs={'class': 'input-field', 'placeholder': '+263771234567'}),
            'contact_email':    forms.EmailInput(attrs={'class': 'input-field'}),
            'contact_email_secondary': forms.EmailInput(attrs={'class': 'input-field'}),
            'phone':            forms.TextInput(attrs={'class': 'input-field'}),
            'physical_address': forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
            'facebook_url':     forms.URLInput(attrs={'class': 'input-field'}),
            'instagram_url':    forms.URLInput(attrs={'class': 'input-field'}),
            'linkedin_url':     forms.URLInput(attrs={'class': 'input-field'}),
            'twitter_url':      forms.URLInput(attrs={'class': 'input-field'}),
            'hero_heading':     forms.TextInput(attrs={'class': 'input-field'}),
            'hero_subheading':  forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
            'about_body':       forms.Textarea(attrs={'class': 'input-field', 'rows': 6}),
            'footer_text':      forms.TextInput(attrs={'class': 'input-field'}),
        }
