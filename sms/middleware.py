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


class DynamicSessionTimeoutMiddleware:
    """
    Middleware để set timeout khác nhau cho chủ nhà và renter.
    - Renter: Timeout ngắn hơn (10 phút mặc định)
    - Chủ nhà: Timeout dài hơn (30 phút mặc định)
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Timeout values in seconds
        self.renter_timeout = getattr(settings, 'RENTER_SESSION_TIMEOUT', 600)  # 10 minutes
        self.owner_timeout = getattr(settings, 'OWNER_SESSION_TIMEOUT', 1800)  # 30 minutes
        
    def __call__(self, request):
        # Set timeout dựa vào loại user
        if request.user.is_authenticated:
            try:
                # Kiểm tra xem user có phải là renter không
                if hasattr(request.user, 'renter'):
                    # User này là renter
                    request.session.set_expiry(self.renter_timeout)
                else:
                    # User này là chủ nhà hoặc admin
                    request.session.set_expiry(self.owner_timeout)
            except Exception:
                # Nếu có lỗi, dùng timeout mặc định
                pass
        
        response = self.get_response(request)
        return response
