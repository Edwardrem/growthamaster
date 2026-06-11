from django import forms
from services.models import Service
from .models import Enquiry


class EnquiryReplyForm(forms.Form):
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'input-field'})
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'input-field', 'rows': 6})
    )


class EnquiryForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True).select_related('category'),
        required=False,
        empty_label='— Select a service (optional) —',
        widget=forms.Select(attrs={'class': 'input-field'}),
    )

    class Meta:
        model = Enquiry
        fields = ('name', 'email', 'phone', 'service', 'message')
        widgets = {
            'name':    forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Your full name'}),
            'email':   forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'your@email.com'}),
            'phone':   forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Phone number (optional)'}),
            'message': forms.Textarea(attrs={'class': 'input-field', 'rows': 5, 'placeholder': 'Tell us about your enquiry...'}),
        }
