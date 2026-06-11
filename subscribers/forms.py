from django import forms


class SubscribeForm(forms.Form):
    first_name = forms.CharField(
        max_length=60, required=False,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'First name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Your email address'})
    )
