"""
Custom CSRF failure view to handle expired CSRF tokens gracefully.
"""
from django.shortcuts import render
from django.middleware.csrf import REASON_NO_REFERER, REASON_NO_CSRF_COOKIE
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def csrf_failure(request, reason=""):
    """
    Custom view for CSRF validation failures.
    Shows a friendly message and redirects back to login for expired sessions.
    """
    ctx = {
        'message': 'Phiên làm việc của bạn đã hết hạn.',
        'reason': reason,
        'no_referer': reason == REASON_NO_REFERER,
        'no_cookie': reason == REASON_NO_CSRF_COOKIE,
    }
    
    # Provide user-friendly messages based on failure reason
    if reason == REASON_NO_CSRF_COOKIE:
        ctx['message'] = 'Trình duyệt của bạn không chấp nhận cookies. Vui lòng bật cookies và thử lại.'
    elif reason == REASON_NO_REFERER:
        ctx['message'] = 'Yêu cầu không hợp lệ. Vui lòng thử lại.'
    else:
        ctx['message'] = 'Phiên làm việc của bạn đã hết hạn. Vui lòng đăng nhập lại.'
    
    return render(request, 'sms/csrf_failure.html', ctx, status=403)
