from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from django.utils.html import escape
from django.views.generic import TemplateView
from django.shortcuts import render

from services.models import ServiceCategory
from portfolio.models import PortfolioItem

# Users created by /seed. Dev-only credentials — change/remove before production.
SEED_USERS = [
    {'username': 'admin', 'email': 'admin@growthmaster.local', 'password': 'admin1234',
     'is_staff': True, 'is_superuser': True},
    {'username': 'staff', 'email': 'staff@growthmaster.local', 'password': 'staff1234',
     'is_staff': True, 'is_superuser': False},
]

WHY_US = [
    {'icon': 'M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z', 'title': 'Proven Expertise', 'desc': 'A decade of practical consultancy experience across business, development, and research sectors.'},
    {'icon': 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z', 'title': 'Client-Centred', 'desc': 'We listen first. Every solution is tailored to your specific context, goals, and constraints.'},
    {'icon': 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z', 'title': 'Results-Driven', 'desc': 'We measure success by your outcomes — funding secured, strategies executed, goals achieved.'},
    {'icon': 'M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064', 'title': 'Local & Regional', 'desc': 'Deep roots in Zimbabwe with a regional perspective — we understand the business environment.'},
]


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = ServiceCategory.objects.prefetch_related('services').order_by('order')[:3]
        ctx['portfolio_featured'] = PortfolioItem.objects.filter(is_active=True, is_featured=True)[:3]
        ctx['why_us_default'] = WHY_US
        return ctx


class AboutView(TemplateView):
    template_name = 'core/about.html'


def seed_users(request):
    """Dev-only endpoint that seeds a set of login users into the database.

    Guarded to DEBUG mode only — creating login-capable accounts (including a
    superuser) must never be reachable in production. Idempotent: re-running
    updates the flags/password of existing users rather than duplicating them.
    """
    if not settings.DEBUG:
        raise Http404()

    User = get_user_model()
    rows = []
    for spec in SEED_USERS:
        user, created = User.objects.get_or_create(
            username=spec['username'],
            defaults={'email': spec['email']},
        )
        user.email = spec['email']
        user.is_staff = spec['is_staff']
        user.is_superuser = spec['is_superuser']
        user.set_password(spec['password'])
        user.save()
        rows.append((spec['username'], spec['password'], spec['email'],
                     'superuser' if spec['is_superuser'] else ('staff' if spec['is_staff'] else 'user'),
                     'created' if created else 'updated'))

    body = ['<h1>Seeded users</h1>',
            '<p style="color:#B13921">Dev-only endpoint (active because DEBUG=True). '
            'Change these credentials before any production use.</p>',
            '<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;font-family:sans-serif">',
            '<tr><th>Username</th><th>Password</th><th>Email</th><th>Role</th><th>Result</th></tr>']
    for username, password, email, role, result in rows:
        body.append(
            f'<tr><td>{escape(username)}</td><td><code>{escape(password)}</code></td>'
            f'<td>{escape(email)}</td><td>{role}</td><td>{result}</td></tr>')
    body.append('</table>')
    body.append('<p><a href="/manage/">→ Go to the management portal</a></p>')
    return HttpResponse('\n'.join(body))


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)
