# URL ID Obfuscation Implementation Guide

## 🎯 Mục Đích

Encode các integer IDs trong URLs để:
- ✅ Tránh enumeration attacks (không đoán được IDs)
- ✅ Che giấu số lượng records trong database
- ✅ URLs thân thiện và bảo mật hơn
- ✅ Dễ implement, không cần thay đổi database

## 📦 Đã Cài Đặt

### 1. Thư Viện
```bash
pip install hashids==1.3.1  # ✅ Installed
```

### 2. Files Tạo Mới

- `sms/utils/id_encoder.py` - Core encode/decode functions
- `sms/utils/hashid_converter.py` - Django URL converter
- `sms/templatetags/id_encoder.py` - Template filters/tags

### 3. Settings Configuration

```python
# CollegeERP/settings.py
HASHIDS_SALT = 'your-secret-salt'  # ⚠️ Đổi trong production!
HASHIDS_MIN_LENGTH = 8
HASHIDS_ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
```

## 🚀 Cách Sử Dụng

### Method 1: Using Template Filters (Recommended for Existing Code)

**Không cần thay đổi URLs.py**, chỉ update templates:

#### Before:
```html
<a href="{% url 'bill_detail' bill_id=bill.id %}">View Bill #{{ bill.id }}</a>
```

#### After:
```html
{% load id_encoder %}
<a href="{% url 'bill_detail' bill_id=bill.id|encode_id %}">View Bill #{{ bill.id|encode_id }}</a>
```

**Views giữ nguyên:**
```python
def bill_detail_view(request, bill_id):
    # bill_id vẫn là integer như bình thường
    bill = get_object_or_404(Hoadon, pk=bill_id)
    ...
```

### Method 2: Using URL Converter (For New URLs)

Cho URLs mới hoặc refactor URLs:

#### urls.py:
```python
from django.urls import path, register_converter
from sms.utils.hashid_converter import HashidConverter

# Register converter
register_converter(HashidConverter, 'hashid')

urlpatterns = [
    # Old way (integer)
    # path('bill/<int:bill_id>/detail/', views.bill_detail, name='bill_detail'),
    
    # New way (hashid) - URL automatically converts
    path('bill/<hashid:bill_id>/detail/', views.bill_detail, name='bill_detail_secure'),
]
```

#### Views không thay đổi:
```python
def bill_detail(request, bill_id):
    # bill_id tự động được decode thành integer
    bill = get_object_or_404(Hoadon, pk=bill_id)
    ...
```

#### Templates:
```html
<a href="{% url 'bill_detail_secure' bill_id=bill.id %}">View</a>
<!-- Django tự động encode bill.id thành hash -->
```

## 📋 Implementation Examples

### Example 1: Bill URLs (Priority - Sensitive Data)

#### Step 1: Update URLs (Optional - cho URLs mới)

```python
# sms/urls.py
from django.urls import register_converter
from sms.utils.hashid_converter import HashidConverter

register_converter(HashidConverter, 'hashid')

urlpatterns = [
    # Bills - Secure versions
    path('bill/<hashid:bill_id>/detail/', views.bill_detail_view, name='bill_detail_secure'),
    path('bill/<hashid:bill_id>/update/', views.update_bill_view, name='update_bill_secure'),
    path('bill/<hashid:bill_id>/pdf/', views.generate_bill_pdf, name='bill_pdf_secure'),
    
    # Keep old URLs for backward compatibility (will deprecate later)
    path('bill/<int:bill_id>/detail/', views.bill_detail_view, name='bill_detail'),
    ...
]
```

#### Step 2: Update Templates

```html
{% load id_encoder %}

<!-- Bill list -->
{% for bill in bills %}
    <tr>
        <td>{{ bill.ten }}</td>
        <td>
            <!-- Use encoded ID in URL -->
            <a href="{% url 'bill_detail_secure' bill_id=bill.id %}" class="btn btn-sm btn-primary">
                View
            </a>
            <a href="{% url 'bill_pdf_secure' bill_id=bill.id %}" class="btn btn-sm btn-secondary">
                PDF
            </a>
        </td>
    </tr>
{% endfor %}
```

### Example 2: Issue/Notification URLs

```python
# sms/urls.py
urlpatterns = [
    path('issues/<hashid:issue_id>/', views.issue_detail, name='issue_detail_secure'),
    path('issues/<hashid:issue_id>/comment/', views.add_issue_comment, name='add_issue_comment_secure'),
    path('notifications/<hashid:notification_id>/read/', views.mark_notification_read, name='mark_notification_read_secure'),
]
```

```html
{% load id_encoder %}

<!-- Notification list -->
{% for notification in notifications %}
    <a href="{% url 'issue_detail_secure' issue_id=notification.related_issue_id %}">
        {{ notification.title }}
    </a>
{% endfor %}
```

### Example 3: House & Location URLs

```python
# sms/urls.py
urlpatterns = [
    path('location/<hashid:loc_id>/bills/', views.bill_list_view, name='bill_list_secure'),
    path('house/<hashid:house_id>/create-bill/', views.create_bill_view, name='create_bill_secure'),
    path('location/<hashid:loc_id>/houses/', views.house_list, name='house_list_secure'),
]
```

### Example 4: Contract URLs

```python
urlpatterns = [
    path('contract/<hashid:contract_id>/detail/', views.contract_detail, name='contract_detail_secure'),
    path('house/<hashid:house_id>/contracts/', views.house_contracts, name='house_contracts_secure'),
]
```

## 🔧 Utility Functions

### In Python Code (Views, Utils)

```python
from sms.utils.id_encoder import encode_id, decode_id

# Encode an ID
bill_id = 123
encoded = encode_id(bill_id)
print(encoded)  # Output: 'jR7qKm3p'

# Decode a hash
hash_str = 'jR7qKm3p'
decoded = decode_id(hash_str)
print(decoded)  # Output: 123

# Multiple IDs
from sms.utils.id_encoder import encode_multiple, decode_multiple

encoded = encode_multiple(123, 456, 789)
decoded = decode_multiple(encoded)
```

### In Templates

```html
{% load id_encoder %}

<!-- Encode ID -->
{{ bill.id|encode_id }}

<!-- In URLs -->
<a href="/bill/{{ bill.id|encode_id }}/detail/">View</a>

<!-- Or with url tag -->
<a href="{% url 'bill_detail' bill_id=bill.id|encode_id %}">View</a>

<!-- Hide ID from display -->
Bill Reference: {{ bill.id|encode_id }}  <!-- Shows: jR7qKm3p instead of 123 -->
```

## 🎬 Migration Strategy

### Phase 1: Add Secure URLs (Keep Old URLs)

```python
# sms/urls.py
urlpatterns = [
    # NEW - Secure URLs
    path('bill/<hashid:bill_id>/detail/', views.bill_detail_view, name='bill_detail_secure'),
    
    # OLD - Keep for backward compatibility
    path('bill/<int:bill_id>/detail/', views.bill_detail_view, name='bill_detail'),
]
```

### Phase 2: Update Templates Gradually

```html
<!-- Update templates to use secure URLs -->
{% url 'bill_detail_secure' bill_id=bill.id %}  <!-- New -->
{% url 'bill_detail' bill_id=bill.id %}  <!-- Old -->
```

### Phase 3: Monitor & Test

- Test all links work
- Check emails still work
- Verify notifications URLs
- Test API endpoints

### Phase 4: Deprecate Old URLs (After Testing)

```python
# Remove old integer URLs after confirming secure URLs work
urlpatterns = [
    path('bill/<hashid:bill_id>/detail/', views.bill_detail_view, name='bill_detail'),
    # Removed: path('bill/<int:bill_id>/detail/', ...)
]
```

## 🔐 Security Benefits

### Before (Integer IDs):
```
URL: /bill/123/detail/
URL: /bill/124/detail/  ← Attacker can increment
URL: /bill/125/detail/  ← Easy enumeration
```

**Problems:**
- ❌ Can guess other bill IDs
- ❌ Know total number of bills
- ❌ Easy to automate scraping
- ❌ Privacy leak

### After (Encoded IDs):
```
URL: /bill/jR7qKm3p/detail/
URL: /bill/vYz8Pn2L/detail/  ← Cannot guess pattern
URL: /bill/mQw4Xr9K/detail/  ← No correlation
```

**Benefits:**
- ✅ Cannot guess other IDs
- ✅ Hide database size
- ✅ Hard to enumerate
- ✅ Better privacy

## ⚙️ Configuration Options

```python
# CollegeERP/settings.py

# Salt - Change this to something unique for your app
HASHIDS_SALT = 'your-unique-secret-salt-min-32-chars-long'

# Minimum length of encoded strings
HASHIDS_MIN_LENGTH = 8  # e.g., 'jR7qKm3p' (8 chars)

# Alphabet (characters used in encoding)
HASHIDS_ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

# Optional: Exclude confusing characters
HASHIDS_ALPHABET = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789'  # No i,l,o,0,1
```

## 🧪 Testing

### Test in Django Shell

```python
python manage.py shell

from sms.utils.id_encoder import encode_id, decode_id

# Test encoding
encoded = encode_id(123)
print(f"123 → {encoded}")

# Test decoding
decoded = decode_id(encoded)
print(f"{encoded} → {decoded}")

# Should output:
# 123 → jR7qKm3p
# jR7qKm3p → 123
```

### Test in Browser

1. Open bill list page
2. Check URL: `/bill/jR7qKm3p/detail/` (not `/bill/123/detail/`)
3. Try to manually change hash → Should get 404
4. Copy/share URL → Hash should work

## 📊 URLs Priority for Migration

### High Priority (Sensitive Data):
1. ✅ Bills: `/bill/<id>/`
2. ✅ Payments: `/payment/<id>/`
3. ✅ Contracts: `/contract/<id>/`
4. ✅ Issues: `/issues/<id>/`
5. ✅ Notifications: `/notifications/<id>/`

### Medium Priority:
6. Houses: `/house/<id>/`
7. Locations: `/location/<id>/`
8. Renters: `/renter/<id>/`

### Low Priority (Internal/Admin):
9. Teachers: `/teacher/<id>/`
10. Students: `/student/<id>/`
11. Classes: `/class/<id>/`

## 🚨 Important Notes

1. **Salt Security**: 
   - Change `HASHIDS_SALT` in production
   - Keep it secret (like SECRET_KEY)
   - Don't commit to git if using environment variables

2. **Backward Compatibility**:
   - Keep old URLs during migration
   - Test thoroughly before removing
   - Update bookmarks/saved links

3. **Performance**:
   - Encoding/decoding is very fast (microseconds)
   - No database changes needed
   - No performance impact

4. **Limitations**:
   - Hash length increases with ID size
   - Not true encryption (can be decoded with salt)
   - Use HTTPS for full security

## 📝 Quick Reference Commands

```python
# Encode
from sms.utils.id_encoder import encode_id
hash_str = encode_id(123)

# Decode
from sms.utils.id_encoder import decode_id
id_int = decode_id('jR7qKm3p')

# In template
{% load id_encoder %}
{{ object.id|encode_id }}
```

## ✅ Checklist

Migration checklist cho từng URL pattern:

- [ ] Add hashid converter to urls.py
- [ ] Create secure URL pattern
- [ ] Update templates to use secure URLs
- [ ] Test URL works in browser
- [ ] Test encode/decode correct
- [ ] Check emails/notifications still work
- [ ] Update API documentation
- [ ] Remove old URL pattern (after testing)

---

**Ready to implement!** Start with bills and payments (high priority), test thoroughly, then expand to other areas.
