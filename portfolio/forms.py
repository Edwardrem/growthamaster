from django import forms
from .models import PortfolioItem


class PortfolioItemForm(forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = (
            'title', 'media_type', 'category', 'description',
            'thumbnail', 'media_url', 'embed_code', 'media_file',
            'alt_text', 'caption', 'client_name', 'project_date',
            'is_featured', 'is_active', 'order',
        )
        widgets = {
            'title':        forms.TextInput(attrs={'class': 'input-field'}),
            'media_type':   forms.Select(attrs={'class': 'input-field'}),
            'category':     forms.Select(attrs={'class': 'input-field'}),
            'description':  forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
            'media_url':    forms.URLInput(attrs={'class': 'input-field'}),
            'embed_code':   forms.Textarea(attrs={'class': 'input-field', 'rows': 4,
                                                   'placeholder': 'Paste full embed code here'}),
            'alt_text':     forms.TextInput(attrs={'class': 'input-field'}),
            'caption':      forms.TextInput(attrs={'class': 'input-field'}),
            'client_name':  forms.TextInput(attrs={'class': 'input-field'}),
            'project_date': forms.DateInput(attrs={'class': 'input-field', 'type': 'date'}),
            'order':        forms.NumberInput(attrs={'class': 'input-field'}),
        }
