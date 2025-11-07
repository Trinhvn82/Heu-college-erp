# Access Control & Data Isolation Checklist

## Tổng quan
Document này trình bày cách kiểm tra và đảm bảo rằng mỗi role (Renter/Landlord) chỉ được:
1. Truy cập vào các view được phép
2. Chỉ xem/thao tác data của chính họ

---

## 1. AUTHENTICATION LAYER - Kiểm tra đăng nhập

### ✅ Tất cả views đều có `@login_required` decorator

```python
@login_required
def renter_dashboard(request):
    ...

@login_required  
def bill_detail_view(request, bill_id):
    ...
```

**Mục đích**: Chặn user chưa đăng nhập
**Kiểm tra**: 
```bash
# Test: Access URL khi chưa login → Phải redirect về /accounts/login/
curl -I http://127.0.0.1:8000/sms/renter/dashboard/
# Expected: 302 Redirect to login
```

---

## 2. AUTHORIZATION LAYER - Kiểm tra quyền truy cập

### ✅ Helper Function: `get_object_or_forbidden()`

**File**: `sms/views.py` (dòng 62-120)

```python
def get_object_or_forbidden(model, user, error_message, **kwargs):
    """
    Centralized access control cho tất cả models
    
    Returns:
        (object, None) - nếu có quyền
        (None, redirect_response) - nếu không có quyền
    """
    obj = get_object_or_404(model, **kwargs)
    
    # Superuser bypass
    if user.is_superuser:
        return obj, None
    
    # Check theo từng model
    if model == Hoadon:
        is_landlord = obj.house.loc.chu_id == user.id
        is_renter = obj.renter and obj.renter.user_id == user.id
        
        if not is_landlord and not is_renter:
            return None, redirect_with_error()
    
    # Similar checks for Location, House, HouseRenter, etc.
```

**Cách hoạt động**:
- Lấy object từ database
- Check xem user có quyền không (landlord hoặc renter)
- Return object HOẶC redirect với error message

---

## 3. DATA ISOLATION - Chỉ lấy data của user

### A. Renter Views

#### ✅ `renter_dashboard` (dòng 1695)
```python
def renter_dashboard(request):
    # 1. Verify renter identity
    renter = Renter.objects.get(user=request.user)  # ← KEY: get ONLY current user's renter
    
    # 2. Filter contracts by renter
    contracts = HouseRenter.objects.filter(
        renter=renter,  # ← Only this renter's contracts
        house__isnull=False
    )
    
    # 3. Filter bills by renter
    bills = Hoadon.objects.filter(
        renter=renter,  # ← Only this renter's bills
        house__isnull=False
    )
```

**Kiểm tra**:
```python
# Test trong Django shell
from django.contrib.auth.models import User
from sms.models import Renter, Hoadon

# Login as renter1
user1 = User.objects.get(username='renter1')
renter1 = Renter.objects.get(user=user1)

# Query bills
bills = Hoadon.objects.filter(renter=renter1)
print(f"Renter1 bills: {bills.count()}")

# Verify không có bill của renter khác
for bill in bills:
    assert bill.renter.id == renter1.id, "DATA LEAK!"
```

---

#### ✅ `renter_bills` (dòng 1765)
```python
def renter_bills(request):
    renter = Renter.objects.get(user=request.user)  # ← KEY
    
    bills = Hoadon.objects.filter(
        renter=renter,  # ← Filter by current renter
        house__isnull=False
    )
```

---

#### ✅ `renter_issue_list` (dòng 6460)
```python
def renter_issue_list(request):
    renter = Renter.objects.get(user=request.user)  # ← KEY
    
    issues = IssueReport.objects.filter(
        renter=renter  # ← Only this renter's issues
    )
```

---

### B. Shared Views (Landlord + Renter)

#### ✅ `bill_detail_view` (dòng 5462)
```python
def bill_detail_view(request, bill_id):
    # 1. Validate access using helper function
    hoadon, error_response = validate_bill_access(request, bill_id)
    if error_response:
        return error_response  # ← Redirect nếu không có quyền
    
    # 2. Check role để hiển thị UI phù hợp
    is_renter = hoadon.renter and hoadon.renter.user_id == request.user.id
    
    # 3. Chọn template base
    base_template = "layouts/renter_base.html" if is_renter else "layouts/rental_base.html"
```

**Flow kiểm tra**:
1. `validate_bill_access()` → gọi `get_object_or_forbidden()`
2. Check: `is_landlord OR is_renter` → OK
3. Nếu không match → Return error và redirect

---

#### ✅ `issue_detail` (dòng 6482)
```python
def issue_detail(request, issue_id):
    issue = get_object_or_404(IssueReport, id=issue_id)
    
    # Check access
    is_renter = issue.renter and issue.renter.user == request.user
    is_landlord = issue.house.loc.chu == request.user
    
    if not (is_renter or is_landlord):
        return HttpResponse("Unauthorized", status=403)  # ← Block
```

---

## 4. TESTING CHECKLIST

### Test Case 1: Renter không xem được data của renter khác
```python
# Setup
renter1 = User.objects.get(username='renter1')
renter2 = User.objects.get(username='renter2')

# Test: Login as renter1
client.login(username='renter1', password='password')

# Try to access renter2's bill
bill_renter2 = Hoadon.objects.filter(renter__user=renter2).first()
response = client.get(f'/sms/bill/{bill_renter2.id}/detail/')

# Expected: 403 hoặc redirect với error message
assert response.status_code in [302, 403]
```

---

### Test Case 2: Renter dashboard chỉ hiển thị data của renter
```python
# Login as renter1
client.login(username='renter1', password='password')
response = client.get('/sms/renter/dashboard/')

# Check context data
contracts = response.context['contracts']
bills = response.context['bills']

# Verify all contracts belong to renter1
for contract in contracts:
    assert contract.renter.user.username == 'renter1'

# Verify all bills belong to renter1  
for bill in bills:
    assert bill.renter.user.username == 'renter1'
```

---

### Test Case 3: Direct URL access với ID khác
```bash
# Login as renter1 (ID: 5)
# Try to access renter2's dashboard (if such URL exists with ID)
curl -b cookies.txt http://127.0.0.1:8000/sms/bill/999/detail/

# Expected: Error message hoặc redirect
# Should NOT show bill details
```

---

## 5. COMMON VULNERABILITIES TO CHECK

### ❌ Missing Filter
```python
# BAD - Lấy tất cả bills
bills = Hoadon.objects.all()  # ← WRONG! Exposes all data
```

### ✅ Correct Filter
```python
# GOOD - Chỉ lấy bills của renter
bills = Hoadon.objects.filter(renter=current_renter)
```

---

### ❌ Không check ownership trước khi update
```python
# BAD
def update_bill(request, bill_id):
    bill = get_object_or_404(Hoadon, id=bill_id)
    bill.status = request.POST['status']  # ← WRONG! Không check ownership
    bill.save()
```

### ✅ Check ownership trước
```python
# GOOD
def update_bill(request, bill_id):
    bill, error = validate_bill_access(request, bill_id)
    if error:
        return error  # ← Block nếu không có quyền
    
    bill.status = request.POST['status']
    bill.save()
```

---

### ❌ Query dựa vào user input không validate
```python
# BAD
def get_contract(request):
    contract_id = request.GET.get('id')
    contract = HouseRenter.objects.get(id=contract_id)  # ← WRONG! Không check owner
    return JsonResponse({...})
```

### ✅ Validate ownership
```python
# GOOD
def get_contract(request):
    contract_id = request.GET.get('id')
    contract = get_object_or_404(HouseRenter, id=contract_id)
    
    # Check owner
    if contract.house.loc.chu != request.user:
        return HttpResponseForbidden()
    
    return JsonResponse({...})
```

---

## 6. AUDIT LOG - Debug Access

### Đã thêm logging vào `renter_dashboard`:
```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"Renter Dashboard - User: {request.user.username}, Renter ID: {renter.id}")
logger.info(f"Contracts count: {contracts.count()}")
logger.info(f"Bills count: {bills.count()}")

for c in contracts:
    logger.info(f"  - Contract: {c.house.ten}, Renter: {c.renter.hoten} (ID: {c.renter.id})")

for b in bills[:5]:
    logger.info(f"  - Bill ID: {b.id}, Renter: {b.renter.hoten} (ID: {b.renter.id})")
```

**Cách kiểm tra**:
1. Access dashboard: http://127.0.0.1:8000/sms/renter/dashboard/
2. Check terminal logs
3. Verify tất cả contracts/bills có cùng renter ID

---

## 7. SECURITY BEST PRACTICES

### ✅ Implement
1. **Always filter by user**: `objects.filter(renter=current_renter)`
2. **Use helper functions**: `get_object_or_forbidden()`, `validate_bill_access()`
3. **Check before modify**: Validate ownership trước khi update/delete
4. **Use `@login_required`**: Trên tất cả views
5. **Log sensitive operations**: Track ai access data gì
6. **Return proper HTTP codes**: 403 Forbidden, 404 Not Found

### ❌ Avoid
1. **Không dùng `.all()`** trên sensitive models
2. **Không trust user input**: Luôn validate ID, parameters
3. **Không expose primary keys**: Dùng UUID nếu có thể
4. **Không skip ownership check**: Kể cả khi ID từ hidden field

---

## 8. QUICK AUDIT COMMANDS

### Check tất cả renter views có @login_required:
```bash
grep -n "def renter_" sms/views.py | grep -B1 "@login_required"
```

### Check tất cả queries có filter by user:
```bash
grep -n "Hoadon.objects" sms/views.py | grep -v "filter(renter"
# Kết quả trống = GOOD
# Có kết quả = Cần review
```

### Check hardcoded user IDs:
```bash
grep -n "user_id.*=" sms/views.py | grep -E "[0-9]+"
# Không nên có hardcoded IDs
```

---

## 9. PENETRATION TEST SCENARIOS

### Scenario 1: Horizontal Privilege Escalation
```
Attacker: Renter A (user_id=5)
Target: Renter B's bill (bill_id=100, renter_id=10)

Attack Vector:
1. Login as Renter A
2. Try: GET /sms/bill/100/detail/
3. Try: POST /sms/bill/100/comment/ với malicious data

Expected Result:
- 403 Forbidden hoặc redirect với error
- Không trả về data của Renter B
```

### Scenario 2: Direct Object Reference
```
Attacker: Renter A
Target: Guess other bill IDs

Attack Vector:
1. Login as Renter A  
2. Note own bill ID: 50
3. Try sequential IDs: 51, 52, 53...

Expected Result:
- Tất cả requests với ID không thuộc Renter A đều bị block
- Không leak info về bills khác
```

### Scenario 3: Parameter Tampering
```
Attacker: Renter A
Target: Change renter_id in form data

Attack Vector:
1. Login as Renter A
2. POST /sms/bill/50/comment/
   Data: {renter_id: 10, comment: "hack"}

Expected Result:
- Backend KHÔNG dùng renter_id từ form
- Backend dùng request.user để xác định renter
- Comment được gắn đúng renter của user đăng nhập
```

---

## 10. SUMMARY CHECKLIST

### ✅ Views Layer
- [ ] Tất cả renter views có `@login_required`
- [ ] Verify user là renter: `Renter.objects.get(user=request.user)`
- [ ] Redirect nếu không phải renter

### ✅ Data Layer  
- [ ] Tất cả queries có filter by `renter=current_renter`
- [ ] Không dùng `.all()` trên Hoadon, HouseRenter
- [ ] Prefetch related data cũng được filtered

### ✅ Access Control Layer
- [ ] Dùng `get_object_or_forbidden()` cho detail views
- [ ] Check `is_landlord OR is_renter` trước khi cho access
- [ ] Return 403/redirect nếu không match

### ✅ Testing
- [ ] Test cross-renter access → Blocked
- [ ] Test direct URL với ID khác → Blocked  
- [ ] Test parameter tampering → Ignored
- [ ] Check logs để verify đúng renter

### ✅ Security Headers
- [ ] Template không expose sensitive IDs
- [ ] CSRF protection enabled
- [ ] XSS protection trong forms

---

## KẾT LUẬN

Hệ thống hiện tại đã implement đầy đủ:

1. ✅ **Authentication**: `@login_required` trên tất cả views
2. ✅ **Authorization**: `get_object_or_forbidden()` check ownership
3. ✅ **Data Isolation**: Filter by `renter=current_renter` 
4. ✅ **Audit Logging**: Log access để debug
5. ✅ **Proper Redirects**: Redirect về trang phù hợp khi access denied

**Renter chỉ có thể**:
- Xem dashboard với contracts/bills CỦA MÌNH
- Xem chi tiết bill CỦA MÌNH
- Comment trên bill CỦA MÌNH
- Báo cáo issue cho nhà ĐANG THUÊ
- Xem notification VỀ MÌNH

**Renter KHÔNG thể**:
- Xem bill/contract của renter khác
- Access landlord views (locations, houses management)
- Modify data không thuộc về mình
- Bypass ownership checks bằng URL manipulation
