# Session Timeout Configuration Guide

## 📋 Tổng Quan

Hệ thống đã được cấu hình để có **timeout khác nhau** cho 2 loại user:

| User Type | Timeout | Lý do |
|-----------|---------|-------|
| **Renter (Người thuê)** | 10 phút | Bảo mật cao hơn, thông tin cá nhân nhạy cảm |
| **Chủ nhà / Admin** | 30 phút | Thuận tiện quản lý, ít rủi ro |

## 🔧 Cấu Hình Đã Thực Hiện

### 1. File: `CollegeERP/settings.py`

```python
# Session Configuration
SESSION_COOKIE_AGE = 1800  # Default 30 minutes (for owners)
SESSION_SAVE_EVERY_REQUEST = True  # Refresh session on every request

# Custom timeout for different user types
RENTER_SESSION_TIMEOUT = 600   # 10 minutes for renters
OWNER_SESSION_TIMEOUT = 1800   # 30 minutes for owners and admin
```

### 2. File: `sms/middleware.py`

Tạo mới class `DynamicSessionTimeoutMiddleware`:
- Chạy sau `AuthenticationMiddleware`
- Kiểm tra user type (renter hay owner)
- Set `request.session.set_expiry()` tương ứng

### 3. Middleware Order

```python
MIDDLEWARE = [
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'sms.middleware.DynamicSessionTimeoutMiddleware',  # ← Vị trí quan trọng!
    ...
]
```

## 🔄 Cách Hoạt Động

### Flow Diagram

```
┌─────────────┐
│ User Login  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│ AuthenticationMiddleware       │
│ (Xác thực user)                 │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ DynamicSessionTimeoutMiddleware │
│ Check: hasattr(user, 'renter')? │
└──────┬──────────────────────────┘
       │
       ├─── YES ──► Set timeout = 600s (10 min)
       │
       └─── NO ───► Set timeout = 1800s (30 min)
```

### Session Lifecycle

1. **Login**: User đăng nhập, timeout được set theo user type
2. **Activity**: Mỗi request (page load, HTMX call) → reset timer về 0
3. **Idle**: Không có hoạt động → timer đếm ngược
4. **Timeout**: Hết thời gian → session expire → redirect login

## 🧪 Hướng Dẫn Test

### Test 1: Renter Timeout (10 phút)

```bash
# Bước 1: Login với renter account
# URL: http://localhost:8000/renter-login/

# Bước 2: Mở browser DevTools Console và chạy:
console.log("Login time:", new Date().toLocaleTimeString());

# Bước 3: ĐỂ IDLE 10 phút (không click, không refresh)

# Bước 4: Sau 10 phút, click vào bất kỳ link nào
# → Kết quả: Redirect về trang login

# Bước 5: Check console
console.log("Current time:", new Date().toLocaleTimeString());
```

### Test 2: Owner Timeout (30 phút)

```bash
# Bước 1: Login với owner/admin account
# URL: http://localhost:8000/accounts/login/

# Bước 2: Mở DevTools Console:
console.log("Login time:", new Date().toLocaleTimeString());

# Bước 3: ĐỂ IDLE 30 phút

# Bước 4: Sau 30 phút, click link
# → Kết quả: Redirect về login
```

### Test 3: Session Refresh (Auto-extend)

```bash
# Test với bất kỳ account nào

# Bước 1: Login
# Bước 2: Liên tục thao tác (click links, navigate pages)
# Bước 3: Làm việc trong 1 giờ với hoạt động liên tục

# → Kết quả: Session KHÔNG BAO GIỜ expire
# (Vì SESSION_SAVE_EVERY_REQUEST = True)
```

### Test 4: Check Session trong Database

```bash
# Terminal 1: Run Django shell
python manage.py shell

# Trong shell:
from django.contrib.sessions.models import Session
from info.models import User
from datetime import datetime

# Get first active session
now = datetime.now()
session = Session.objects.filter(expire_date__gte=now).first()

if session:
    data = session.get_decoded()
    user_id = data.get('_auth_user_id')
    user = User.objects.get(id=user_id)
    
    print(f"User: {user.username}")
    print(f"Is Renter: {hasattr(user, 'renter')}")
    print(f"Expires at: {session.expire_date}")
    print(f"Time left: {(session.expire_date - now).seconds / 60:.1f} minutes")
```

### Test 5: Sử dụng Script Test

```bash
# Chạy script tự động check configuration
python test_session_timeout.py

# Script sẽ hiển thị:
# - Cấu hình timeout hiện tại
# - Danh sách users (renter vs owner)
# - Active sessions và thời gian còn lại
# - Hướng dẫn test chi tiết
```

## 🐛 Troubleshooting

### Issue 1: Session không expire đúng thời gian

**Nguyên nhân**: 
- Middleware không được thêm vào settings
- Thứ tự middleware sai

**Giải pháp**:
```python
# Check MIDDLEWARE in settings.py
# DynamicSessionTimeoutMiddleware phải SAU AuthenticationMiddleware
```

### Issue 2: Cả 2 loại user đều có cùng timeout

**Nguyên nhân**:
- Logic check renter bị lỗi
- User model không có relationship với Renter

**Debug**:
```python
# Trong Django shell:
from info.models import User

user = User.objects.get(username='<renter_username>')
print(hasattr(user, 'renter'))  # Should return True for renters
print(user.renter)  # Should return Renter object
```

### Issue 3: Session expire ngay lập tức

**Nguyên nhân**:
- SESSION_SAVE_EVERY_REQUEST = False
- Cache backend lỗi

**Giải pháp**:
```python
# settings.py
SESSION_SAVE_EVERY_REQUEST = True  # Must be True
```

## 📊 Monitoring & Logging

### Enable Session Logging

Thêm vào middleware để log mỗi lần set timeout:

```python
# sms/middleware.py
class DynamicSessionTimeoutMiddleware:
    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                if hasattr(request.user, 'renter'):
                    request.session.set_expiry(self.renter_timeout)
                    logger.info(f"Renter {request.user.username}: timeout set to {self.renter_timeout}s")
                else:
                    request.session.set_expiry(self.owner_timeout)
                    logger.info(f"Owner {request.user.username}: timeout set to {self.owner_timeout}s")
            except Exception as e:
                logger.error(f"Error setting timeout: {e}")
        
        response = self.get_response(request)
        return response
```

### View Active Sessions

```bash
# Django Admin
# URL: http://localhost:8000/admin/sessions/session/

# Hoặc trong shell:
python manage.py shell

from django.contrib.sessions.models import Session
from datetime import datetime

active = Session.objects.filter(expire_date__gte=datetime.now())
print(f"Active sessions: {active.count()}")
```

## 🔐 Security Best Practices

1. **Renter Timeout**: Giữ ngắn (10 phút) vì:
   - Thông tin cá nhân nhạy cảm
   - Thường truy cập từ thiết bị công cộng
   - Ít thao tác phức tạp

2. **Owner Timeout**: Dài hơn (30 phút) vì:
   - Cần thời gian làm việc lâu
   - Truy cập từ thiết bị tin cậy
   - Có nhiều thao tác quản lý

3. **SESSION_SAVE_EVERY_REQUEST**: 
   - TRUE: Session tự động extend khi có hoạt động
   - Tránh timeout giữa chừng khi đang làm việc

## 📈 Performance Impact

- **Minimal**: Middleware chỉ chạy khi user authenticated
- **Database writes**: Mỗi request sẽ update session (do SESSION_SAVE_EVERY_REQUEST)
- **Solution**: Sử dụng cache backend cho sessions nếu cần:

```python
# settings.py
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# hoặc
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
```

## 🎯 Customization

### Thay đổi thời gian timeout:

```python
# settings.py
RENTER_SESSION_TIMEOUT = 300   # 5 minutes
OWNER_SESSION_TIMEOUT = 3600   # 60 minutes
```

### Thêm timeout cho group cụ thể:

```python
# sms/middleware.py
def __call__(self, request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            request.session.set_expiry(7200)  # 2 hours for admin
        elif hasattr(request.user, 'renter'):
            request.session.set_expiry(self.renter_timeout)
        else:
            request.session.set_expiry(self.owner_timeout)
```

## ✅ Checklist Hoàn Tất

- [x] Tạo `DynamicSessionTimeoutMiddleware` trong `sms/middleware.py`
- [x] Thêm middleware vào `MIDDLEWARE` trong settings.py
- [x] Set `RENTER_SESSION_TIMEOUT = 600` (10 phút)
- [x] Set `OWNER_SESSION_TIMEOUT = 1800` (30 phút)
- [x] Set `SESSION_SAVE_EVERY_REQUEST = True`
- [x] Tạo script test `test_session_timeout.py`
- [x] Tạo documentation `SESSION_TIMEOUT_GUIDE.md`

## 📞 Support

Nếu có vấn đề, check log:

```bash
# Django logs
tail -f logs/django.log

# Session table
python manage.py dbshell
SELECT * FROM django_session ORDER BY expire_date DESC LIMIT 10;
```
