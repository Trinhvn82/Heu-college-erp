from django.conf import settings
from django.http import HttpResponse

class HTMXLoginRequiredMiddleware:
    """
    When an HTMX request hits a @login_required view and Django responds with a
    redirect to LOGIN_URL, convert it to a 401 so the client can open the login modal.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            is_htmx = request.headers.get('HX-Request') == 'true'
            if is_htmx and getattr(response, 'status_code', None) in (301, 302):
                location = response.headers.get('Location') or response.get('Location')
                login_url = getattr(settings, 'LOGIN_URL', '/accounts/login/')
                if location and login_url and location.startswith(login_url):
                    # Return 401 to trigger client-side handler
                    r = HttpResponse('Unauthorized', status=401)
                    # Optionally add a trigger for custom handlers
                    r['HX-Trigger'] = 'auth-timeout'
                    return r
        except Exception:
            # Fail open; don't block the request pipeline
            return response
        return response
