from django.conf import settings
from django.shortcuts import redirect


class ManagePortalLoginMiddleware:
    """
    Redirect unauthenticated requests to /manage/* to the login page,
    preserving the intended destination via ?next= so the user lands
    back where they wanted after signing in.
    Must appear after AuthenticationMiddleware in MIDDLEWARE.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/manage/') and not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        return self.get_response(request)
