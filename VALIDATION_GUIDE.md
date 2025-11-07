# Hướng dẫn Validation cho Parameter IDs

## Tổng quan

Hệ thống validation đã được cải thiện để đảm bảo:
- ✅ Người dùng chỉ truy cập được tài nguyên thuộc quyền quản lý
- ✅ Hiển thị thông báo lỗi rõ ràng bằng tiếng Việt
- ✅ Redirect về trang danh sách thích hợp khi bị từ chối
- ✅ Superuser có quyền truy cập toàn bộ

## Các Helper Functions

### 1. `get_object_or_forbidden(model, user, error_message, **kwargs)`
Function cơ bản để validate và lấy object. Tự động kiểm tra quyền sở hữu.

**Tham số:**
- `model`: Model class (Location, House, Renter, etc.)
- `user`: request.user
- `error_message`: Thông báo lỗi hiển thị
- `**kwargs`: Điều kiện query (thường là id=value)

**Trả về:**
- `(object, None)` nếu hợp lệ
- `(None, redirect_response)` nếu không hợp lệ

### 2. Các Wrapper Functions Chuyên Biệt

```python
# Location
validate_location_access(request, loc_id)

# House  
validate_house_access(request, house_id)

# Renter
validate_renter_access(request, renter_id)

# Contract (HouseRenter)
validate_contract_access(request, hr_id)

# Bill (Hoadon)
validate_bill_access(request, bill_id)

# Payment (Thanhtoan)
validate_payment_access(request, payment_id)
```

## Cách Sử dụng

### Pattern Chuẩn trong View

```python
@login_required
def edit_house(request, loc_id, house_id):
    # Bước 1: Validate location trước
    loc, error_response = validate_location_access(request, loc_id)
    if error_response:
        return error_response
    
    # Bước 2: Validate house
    house, error_response = validate_house_access(request, house_id)
    if error_response:
        return error_response
    
    # Bước 3: Kiểm tra logic bổ sung nếu cần
    if house.loc_id != loc_id:
        messages.error(request, "Nhà này không thuộc vị trí được chỉ định")
        return redirect('house_list', loc_id)
    
    # Bước 4: Xử lý business logic
    # ...
```

### Ví dụ Đơn giản

```python
@login_required
def view_loc(request, loc_id):
    # Một dòng để validate
    loc, error_response = validate_location_access(request, loc_id)
    if error_response:
        return error_response
    
    # Tiếp tục xử lý
    houses = House.objects.filter(loc_id=loc_id)
    # ...
```

## Quy tắc Ownership

### Location
- Chủ sở hữu: `location.chu == request.user`
- Superuser: Truy cập tất cả

### House
- Chủ sở hữu: `house.loc.chu == request.user`
- Kiểm tra qua location

### Renter
- Chủ sở hữu trực tiếp: `renter.chu_id == request.user.id`
- Hoặc có hợp đồng tại nhà của chủ: `renter.houserenter.house.loc.chu == request.user`

### HouseRenter (Contract)
- Chủ nhà: `contract.house.loc.chu == request.user`

### Hoadon (Bill)
- Chủ nhà: `bill.house.loc.chu == request.user`

### Thanhtoan (Payment)
- Chủ nhà: `payment.hoadon.house.loc.chu == request.user`

## Thông báo Lỗi

### Các loại thông báo
1. **Không có quyền truy cập**: `"Bạn không có quyền truy cập [resource] ID [id]"`
2. **Không tìm thấy**: `"Không tìm thấy dữ liệu yêu cầu"`
3. **Logic sai**: `"Nhà này không thuộc vị trí được chỉ định"`

### Redirect Targets

| Resource | Redirect đến |
|----------|-------------|
| Location | `loc_list` |
| House | `loc_list` |
| Renter | `renter_list` |
| Contract | `loc_list` |
| Bill | `invoice_search` |
| Payment | `invoice_search` |

## Testing

### Chạy Test Suite

```bash
# Test validation
python manage.py test sms.tests_parameter_validation -v 2

# Test tất cả
python manage.py test sms -v 2
```

### Test Cases Bao gồm

1. ✅ Location access & edit validation
2. ✅ House edit validation với location check
3. ✅ Renter edit validation
4. ✅ Contract list validation
5. ✅ Bill detail validation
6. ✅ Payment operations (confirm/delete)
7. ✅ Superuser full access
8. ✅ File upload validation
9. ✅ Invalid ID handling

## Migration từ Code Cũ

### Trước

```python
def edit_loc(request, loc_id):
    if request.user.is_superuser:
        loc = get_object_or_404(Location, id=loc_id)
    else:
        loc = get_object_or_404(Location, id=loc_id, chu=request.user)
    # ...
```

### Sau

```python
def edit_loc(request, loc_id):
    loc, error_response = validate_location_access(request, loc_id)
    if error_response:
        return error_response
    # ...
```

**Lợi ích:**
- 📝 Code ngắn gọn hơn
- 🔒 Validation nhất quán
- 💬 Thông báo lỗi đồng nhất
- ✅ Dễ maintain và test

## Best Practices

1. **Luôn validate trước khi xử lý logic**
   ```python
   obj, err = validate_xxx_access(request, id)
   if err: return err
   ```

2. **Validate theo thứ tự phụ thuộc**
   ```python
   # Location trước
   loc, err = validate_location_access(request, loc_id)
   if err: return err
   
   # House sau (phụ thuộc location)
   house, err = validate_house_access(request, house_id)
   if err: return err
   ```

3. **Kiểm tra logic nghiệp vụ sau validation**
   ```python
   # Đã validate cả loc và house
   # Giờ check logic: house có thuộc loc không?
   if house.loc_id != loc_id:
       messages.error(request, "...")
       return redirect(...)
   ```

4. **Sử dụng messages framework**
   ```python
   messages.error(request, "Thông báo lỗi")
   messages.success(request, "Thành công")
   messages.warning(request, "Cảnh báo")
   ```

## Troubleshooting

### Lỗi: "Không tìm thấy dữ liệu"
- Kiểm tra ID có tồn tại không
- Kiểm tra user có quyền truy cập không

### Lỗi: "Bạn không có quyền..."
- Xác nhận ownership chain đúng
- Kiểm tra superuser status

### Test fails
- Chạy test với `-v 2` để xem chi tiết
- Kiểm tra messages context trong response
- Verify redirect targets đúng

## Tương lai

Có thể mở rộng với:
- [ ] Role-based permissions với django-guardian
- [ ] Audit log cho access denied
- [ ] Rate limiting cho security
- [ ] API endpoint validation
