from django.core.mail import send_mail
from django.conf import settings

def send_login_info_email(renter, password):
    """
    Send login info to renter's email.
    renter: User object (must have email)
    password: plain text password (or set a link to reset)
    """
    if not renter.email:
        return False
    subject = 'Thông tin đăng nhập hệ thống quản lý nhà trọ'
    message = f"Xin chào {renter.get_full_name() or renter.username},\n\nTài khoản của bạn đã được tạo trên hệ thống quản lý nhà trọ.\n\nThông tin đăng nhập:\nEmail: {renter.email}\nTên đăng nhập: {renter.username}\nMật khẩu: {password}\n\nVui lòng đổi mật khẩu sau khi đăng nhập lần đầu.\n\nTrân trọng."
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[renter.email],
            fail_silently=False,
        )
        return True
    except Exception:
        return False
