from django.shortcuts import render, get_object_or_404
from django.views import View

from .forms import SubscribeForm
from .models import Subscriber


class SubscribeView(View):
    def post(self, request):
        form = SubscribeForm(request.POST)
        source = request.POST.get('source', 'footer_form')
        is_htmx = request.headers.get('HX-Request')
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data.get('first_name', '')
            sub, created = Subscriber.objects.get_or_create(
                email=email,
                defaults={'first_name': first_name, 'source': source},
            )
            if not created and not sub.is_active:
                sub.is_active = True
                sub.first_name = first_name or sub.first_name
                sub.save(update_fields=['is_active', 'first_name'])
            if is_htmx:
                return render(request, 'subscribers/partials/subscribe_success.html',
                              {'first_name': first_name or 'there'})
        if is_htmx:
            return render(request, 'subscribers/partials/subscribe_form.html',
                          {'form': form, 'source': source})
        return render(request, 'contacts/contact.html', {'form': form})


class UnsubscribeView(View):
    def get(self, request, token):
        subscriber = get_object_or_404(Subscriber, token=token)
        already_unsubscribed = not subscriber.is_active
        if not already_unsubscribed:
            subscriber.unsubscribe()
        return render(request, 'subscribers/unsubscribe_confirm.html', {
            'subscriber': subscriber,
            'already_unsubscribed': already_unsubscribed,
        })
