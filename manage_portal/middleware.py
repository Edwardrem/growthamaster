from django.http import Http404


class ManagePortal404Middleware:
    """
    Raise Http404 (not 403 or redirect) for any /manage/ request
    made by an unauthenticated user, so the portal is not advertised.
    Must appear after AuthenticationMiddleware in MIDDLEWARE.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/manage/') and not request.user.is_authenticated:
            raise Http404
        return self.get_response(request)
