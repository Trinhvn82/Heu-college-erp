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
        # Bỏ logic trả về 401 và HX-Trigger, chỉ trả về response mặc định
        return response


class DynamicSessionTimeoutMiddleware:
    """
    Middleware thiết lập thời gian hết hạn phiên khác nhau:
    - Renter: 2 phút (cấu hình qua RENTER_SESSION_TIMEOUT)
    - Chủ nhà/Admin: 5 phút (cấu hình qua OWNER_SESSION_TIMEOUT)
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Timeout values in seconds
        self.renter_timeout = getattr(settings, 'RENTER_SESSION_TIMEOUT', 120)  # 2 minutes
        self.owner_timeout = getattr(settings, 'OWNER_SESSION_TIMEOUT', 300)  # 5 minutes
        
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
