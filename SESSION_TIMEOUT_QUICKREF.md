# Session Timeout - Quick Reference Card

## ⚙️ Configuration Summary

```python
# settings.py
RENTER_SESSION_TIMEOUT = 600    # 10 minutes
OWNER_SESSION_TIMEOUT = 1800    # 30 minutes
SESSION_SAVE_EVERY_REQUEST = True
```

## 🎯 Timeout Rules

| User Type | Timeout | Auto-Refresh |
|-----------|---------|--------------|
| Renter | 10 min | ✅ Yes |
| Owner/Admin | 30 min | ✅ Yes |

## 🧪 Quick Tests

### Test 1: Check Configuration
```bash
python test_session_timeout.py
```

### Test 2: Check Active Sessions
```bash
python manage.py check_sessions
python manage.py check_sessions --all
python manage.py check_sessions --username john
```

### Test 3: Manual Browser Test
1. Login as renter
2. Wait 10 minutes (no activity)
3. Click any link → Should redirect to login

## 🔍 Debug Commands

### Django Shell
```python
python manage.py shell

from django.contrib.sessions.models import Session
from django.utils import timezone

# Count active sessions
active = Session.objects.filter(expire_date__gte=timezone.now())
print(f"Active: {active.count()}")

# Check specific session
session = Session.objects.first()
data = session.get_decoded()
user_id = data.get('_auth_user_id')
```

### SQL Query
```sql
-- View all sessions
SELECT * FROM django_session ORDER BY expire_date DESC LIMIT 10;

-- Count active sessions
SELECT COUNT(*) FROM django_session 
WHERE expire_date >= NOW();
```

## 📊 Monitoring

### Check Middleware Order
```python
# settings.py - Must be in this order:
'django.contrib.auth.middleware.AuthenticationMiddleware',
'sms.middleware.DynamicSessionTimeoutMiddleware',  # After Auth!
```

### Enable Logging (Optional)
```python
# Add to sms/middleware.py
import logging
logger = logging.getLogger(__name__)

def __call__(self, request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'renter'):
            logger.info(f"Renter {request.user.username}: 10min timeout")
        else:
            logger.info(f"Owner {request.user.username}: 30min timeout")
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Same timeout for all users | Check middleware is registered and after AuthenticationMiddleware |
| Session expires immediately | Ensure SESSION_SAVE_EVERY_REQUEST = True |
| Timeout not working | Run: `python manage.py check_sessions` to verify |

## 📞 Common Commands

```bash
# Check all active sessions
python manage.py check_sessions

# Include expired sessions
python manage.py check_sessions --all

# Check specific user
python manage.py check_sessions --username renter1

# Test email (bonus)
python test_bill_email.py 123

# Run test script
python test_session_timeout.py
```

## 📁 Files Modified

- ✅ `CollegeERP/settings.py` - Configuration
- ✅ `sms/middleware.py` - DynamicSessionTimeoutMiddleware
- ✅ `test_session_timeout.py` - Test script
- ✅ `sms/management/commands/check_sessions.py` - Django command
- ✅ `SESSION_TIMEOUT_GUIDE.md` - Full documentation

## 🎓 Key Concepts

**Auto-Refresh**: Every request resets the timer
**User Detection**: `hasattr(request.user, 'renter')`
**Dynamic Timeout**: Set per-request via middleware
**Backward Compatible**: Old sessions still work

## ✅ Verification Checklist

- [ ] Run `python test_session_timeout.py`
- [ ] Check middleware in MIDDLEWARE list
- [ ] Test with renter account (10 min)
- [ ] Test with owner account (30 min)
- [ ] Verify auto-refresh works
- [ ] Check `python manage.py check_sessions`

---
**Last Updated**: 2025-11-07
**Version**: 1.0
