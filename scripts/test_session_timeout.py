"""
Script test session timeout cho chủ nhà và renter

Hướng dẫn test:
1. Chạy script này: python test_session_timeout.py
2. Script sẽ hiển thị thông tin cấu hình timeout
3. Để test thực tế:
   - Login với tài khoản renter → Session timeout sau 10 phút
   - Login với tài khoản chủ nhà → Session timeout sau 30 phút
   - Mọi hoạt động sẽ refresh session (SESSION_SAVE_EVERY_REQUEST = True)
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CollegeERP.settings')
django.setup()

from django.conf import settings
from info.models import User
from sms.models import Renter


def check_timeout_config():
    """Kiểm tra cấu hình timeout hiện tại"""
    print("\n" + "="*70)
    print(" SESSION TIMEOUT CONFIGURATION")
    print("="*70)
    
    # Kiểm tra settings
    default_timeout = getattr(settings, 'SESSION_COOKIE_AGE', None)
    renter_timeout = getattr(settings, 'RENTER_SESSION_TIMEOUT', None)
    owner_timeout = getattr(settings, 'OWNER_SESSION_TIMEOUT', None)
    save_every_request = getattr(settings, 'SESSION_SAVE_EVERY_REQUEST', False)
    
    print(f"\n📋 Settings.py Configuration:")
    print(f"   - SESSION_COOKIE_AGE (default): {default_timeout} seconds ({default_timeout/60:.0f} minutes)")
    print(f"   - RENTER_SESSION_TIMEOUT: {renter_timeout} seconds ({renter_timeout/60:.0f} minutes)")
    print(f"   - OWNER_SESSION_TIMEOUT: {owner_timeout} seconds ({owner_timeout/60:.0f} minutes)")
    print(f"   - SESSION_SAVE_EVERY_REQUEST: {save_every_request}")
    
    # Kiểm tra middleware
    print(f"\n🔧 Middleware Configuration:")
    if 'sms.middleware.DynamicSessionTimeoutMiddleware' in settings.MIDDLEWARE:
        middleware_index = settings.MIDDLEWARE.index('sms.middleware.DynamicSessionTimeoutMiddleware')
        auth_index = settings.MIDDLEWARE.index('django.contrib.auth.middleware.AuthenticationMiddleware')
        
        if middleware_index > auth_index:
            print(f"   ✅ DynamicSessionTimeoutMiddleware đã được cài đặt")
            print(f"   ✅ Thứ tự middleware đúng (sau AuthenticationMiddleware)")
        else:
            print(f"   ⚠️  WARNING: DynamicSessionTimeoutMiddleware nên đặt SAU AuthenticationMiddleware")
    else:
        print(f"   ❌ DynamicSessionTimeoutMiddleware CHƯA được thêm vào MIDDLEWARE")
    
    print(f"\n" + "="*70)
    print(" USER ANALYSIS")
    print("="*70)
    
    # Phân tích users
    total_users = User.objects.count()
    renters = Renter.objects.filter(user__isnull=False).select_related('user').count()
    owners = total_users - renters
    
    print(f"\n📊 User Statistics:")
    print(f"   - Tổng số users: {total_users}")
    print(f"   - Số lượng renters có tài khoản: {renters}")
    print(f"   - Số lượng chủ nhà/admin: {owners}")
    
    # Sample users
    print(f"\n👥 Sample Users:")
    
    # Renters
    sample_renters = Renter.objects.filter(user__isnull=False).select_related('user')[:3]
    if sample_renters:
        print(f"\n   RENTERS (Timeout: {renter_timeout/60:.0f} phút):")
        for r in sample_renters:
            print(f"   - {r.user.username} ({r.hoten})")
    
    # Owners
    sample_owners = User.objects.filter(renter__isnull=True)[:3]
    if sample_owners:
        print(f"\n   CHỦ NHÀ/ADMIN (Timeout: {owner_timeout/60:.0f} phút):")
        for u in sample_owners:
            user_type = "Admin" if u.is_superuser else "Chủ nhà"
            print(f"   - {u.username} ({user_type})")
    
    print(f"\n" + "="*70)
    print(" HOW IT WORKS")
    print("="*70)
    
    print("""
🔄 Session Lifecycle:

1. LOGIN:
   - User login vào hệ thống
   - DynamicSessionTimeoutMiddleware check user type
   - Set timeout tương ứng:
     * Renter: 10 phút
     * Chủ nhà/Admin: 30 phút

2. ACTIVITY:
   - Mỗi request (click, load trang, HTMX call)
   - SESSION_SAVE_EVERY_REQUEST = True
   - → Session được refresh, timer reset về 0

3. TIMEOUT:
   - Nếu không có hoạt động trong thời gian timeout
   - Session hết hạn
   - User bị redirect về trang login
   - HTMX request sẽ nhận 401 + trigger 'auth-timeout'

📝 Notes:
   - Timeout chỉ áp dụng khi KHÔNG có hoạt động
   - Mọi thao tác trên trang sẽ reset timer
   - Renter có timeout ngắn hơn vì lý do bảo mật
   - Chủ nhà có timeout dài hơn để thuận tiện quản lý
""")
    
    print("="*70)
    print(" TESTING INSTRUCTIONS")
    print("="*70)
    
    print("""
🧪 Cách test thủ công:

1. TEST RENTER TIMEOUT (10 phút):
   - Login với tài khoản renter
   - Để idle (không thao tác) 10 phút
   - Sau 10 phút, click vào bất kỳ đâu
   - → Sẽ bị redirect về login

2. TEST OWNER TIMEOUT (30 phút):
   - Login với tài khoản chủ nhà
   - Để idle (không thao tác) 30 phút
   - Sau 30 phút, click vào bất kỳ đâu
   - → Sẽ bị redirect về login

3. TEST SESSION REFRESH:
   - Login với bất kỳ tài khoản nào
   - Liên tục thao tác (click, navigate)
   - → Session KHÔNG bao giờ expire (timer luôn reset)

4. TEST TRONG CONSOLE:
   # Check session expiry time
   python manage.py shell
   >>> from django.contrib.sessions.models import Session
   >>> from datetime import datetime
   >>> session = Session.objects.first()
   >>> print(session.expire_date)
   >>> print(datetime.now())
""")
    
    print("="*70)


def list_active_sessions():
    """Hiển thị các session đang active"""
    from django.contrib.sessions.models import Session
    from datetime import datetime
    
    print("\n" + "="*70)
    print(" ACTIVE SESSIONS")
    print("="*70)
    
    now = datetime.now()
    sessions = Session.objects.filter(expire_date__gte=now)[:10]
    
    if not sessions:
        print("\n   Không có session nào đang active")
    else:
        print(f"\n   Tìm thấy {sessions.count()} session(s) active:\n")
        for i, session in enumerate(sessions, 1):
            try:
                data = session.get_decoded()
                user_id = data.get('_auth_user_id')
                
                if user_id:
                    user = User.objects.get(id=user_id)
                    is_renter = hasattr(user, 'renter')
                    user_type = "Renter" if is_renter else "Chủ nhà/Admin"
                    timeout = "10 phút" if is_renter else "30 phút"
                    
                    time_left = (session.expire_date - now).total_seconds() / 60
                    
                    print(f"   {i}. User: {user.username}")
                    print(f"      Type: {user_type}")
                    print(f"      Timeout: {timeout}")
                    print(f"      Expires: {session.expire_date.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"      Time left: {time_left:.1f} minutes")
                    print()
            except Exception as e:
                print(f"   {i}. Session (error decoding): {e}\n")
    
    print("="*70)


if __name__ == "__main__":
    check_timeout_config()
    list_active_sessions()
    
    print("\n✅ Configuration check complete!\n")
