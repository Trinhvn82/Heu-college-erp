# 🚀 Quick Start Testing Guide

## Bắt đầu test ngay trong 5 phút!

### Bước 1: Chạy Migrations
```bash
cd D:\Coding\Python-Code\College-ERP-v1.1
python manage.py makemigrations sms
python manage.py migrate
```

### Bước 2: Chạy Server
```bash
python manage.py runserver
```

### Bước 3: Test Mobile Navbar (Ưu tiên!)
1. Mở browser: http://127.0.0.1:8000/
2. Đăng nhập với tài khoản bất kỳ (renter hoặc landlord)
3. Thu nhỏ cửa sổ browser (width < 992px)
4. Click icon hamburger (3 vạch) ở góc trên phải
5. **✅ Kiểm tra:**
   - Menu có nền màu tím?
   - Text màu trắng rõ ràng?
   - Không có text trắng trên nền trắng?

### Bước 4: Test Renter Flow
```
1. Đăng nhập: Tài khoản RENTER
2. Click menu "Sự cố"
3. Click "Báo sự cố"
4. Điền form + Upload ảnh
5. Submit
6. Kiểm tra sự cố mới xuất hiện
```

### Bước 5: Test Landlord Flow
```
1. Đăng nhập: Tài khoản LANDLORD
2. Click menu "Sự cố"
3. KHÔNG thấy nút "Báo sự cố" ✅
4. Click vào sự cố
5. Click "Xử lý xong"
6. Kiểm tra status "Chờ xác nhận"
```

### Bước 6: Test Renter Confirmation
```
1. Đăng nhập lại: Tài khoản RENTER
2. Vào "Sự cố"
3. Click vào sự cố có status "Chờ xác nhận"
4. Thấy alert vàng với 2 nút:
   - "Xác nhận đã xong" (xanh)
   - "Chưa xong" (vàng)
5. Test cả 2 flows
```

---

## ⚠️ Lưu ý quan trọng

### Nếu gặp lỗi "No migrations to apply"
Có nghĩa là migrations đã chạy rồi → OK, skip bước 1.

### Nếu mobile navbar vẫn bị trắng
1. Hard refresh: `Ctrl + Shift + R` (Windows) hoặc `Cmd + Shift + R` (Mac)
2. Clear cache browser
3. Thử browser khác

### Nếu không thấy "Xác nhận đã xong"
Kiểm tra:
1. Sự cố có status "pending_confirmation"?
2. Đang đăng nhập với đúng tài khoản renter?
3. Đã refresh modal chưa?

---

## 📱 Test Devices

### Desktop
- ✅ Chrome (>= 90)
- ✅ Firefox (>= 88)
- ✅ Edge (>= 90)
- ✅ Safari (>= 14)

### Mobile
- ✅ iPhone Safari
- ✅ Android Chrome
- ✅ iPad Safari

### Responsive Breakpoints
- Desktop: >= 992px
- Tablet: 768px - 991px
- Mobile: < 768px

---

## 🐛 Quick Debug

### Badge không đúng màu?
Check trong browser DevTools → Có bị CSS override không?

### Modal không refresh?
Check browser console → Có lỗi HTMX không?

### Authorization failed?
Check user role → User có đúng quyền không?

---

## ✅ Expected Results

Sau 5 phút test:
- [x] Mobile navbar hiển thị đúng
- [x] Renter có thể tạo sự cố
- [x] Landlord KHÔNG có nút "Báo sự cố"
- [x] Flow xác nhận hoạt động

---

**Thời gian:** ~5 phút  
**Skill level:** Beginner  
**Prerequisites:** Django đã cài, server chạy được

Xem chi tiết: `TESTING_CHECKLIST.md`
