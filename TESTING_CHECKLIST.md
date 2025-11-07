# Hướng dẫn Test Hệ thống Quản lý Sự cố

## 📋 Checklist Test Toàn diện

### 1. Test với Tài khoản RENTER (Khách thuê)

#### 1.1. Đăng nhập và Truy cập
- [ ] Đăng nhập với tài khoản renter
- [ ] Kiểm tra menu "Sự cố" hiển thị trong navbar
- [ ] Click vào "Sự cố" → Vào trang danh sách sự cố của renter

#### 1.2. Báo cáo Sự cố Mới
- [ ] Click nút "Báo sự cố" → Modal hiển thị
- [ ] Chọn nhà/phòng từ dropdown
- [ ] Nhập tiêu đề sự cố (VD: "Điều hòa không hoạt động")
- [ ] Nhập mô tả chi tiết
- [ ] Upload 2-3 hình ảnh (test multi-upload)
- [ ] Kiểm tra preview ảnh hiển thị đúng
- [ ] Click "Gửi báo cáo"
- [ ] **Kiểm tra:**
  - Modal đóng tự động
  - Sự cố mới xuất hiện ở đầu bảng với animation xanh
  - Trạng thái hiển thị "Mới" (badge màu vàng)

#### 1.3. Xem Chi tiết Sự cố
- [ ] Click vào dòng sự cố vừa tạo → Modal detail mở
- [ ] **Kiểm tra 4 tabs:**
  - **Tab Thông tin:** Tiêu đề, mô tả, thời gian, trạng thái
  - **Tab Hình ảnh:** 3 ảnh hiển thị đúng, click mở full size
  - **Tab Bình luận:** Form comment hiển thị
  - **Tab Lịch sử:** Có record "Tạo mới"
- [ ] Đóng modal

#### 1.4. Thêm Comment
- [ ] Mở lại detail modal
- [ ] Vào tab "Bình luận"
- [ ] Nhập comment: "Tôi cần sửa gấp vì trời nóng"
- [ ] Click "Gửi" → Comment xuất hiện ngay (HTMX)
- [ ] Kiểm tra badge "Khách thuê" hiển thị

#### 1.5. Kiểm tra Notification
- [ ] Click icon chuông trên navbar
- [ ] Xem thông báo (nếu có từ landlord)
- [ ] Kiểm tra số badge đỏ giảm khi đọc thông báo

---

### 2. Test với Tài khoản LANDLORD (Chủ nhà)

#### 2.1. Đăng nhập và Kiểm tra Notification
- [ ] Đăng nhập với tài khoản landlord
- [ ] Kiểm tra icon chuông có badge đỏ (thông báo sự cố mới)
- [ ] Click icon chuông → Xem thông báo "Sự cố mới được báo"
- [ ] Click "Xem" → Vào trang danh sách sự cố

#### 2.2. Xem Danh sách Sự cố
- [ ] Menu "Sự cố" hiển thị
- [ ] Vào trang danh sách sự cố landlord
- [ ] **Kiểm tra:**
  - Không có nút "Báo sự cố" (chỉ renter mới có)
  - Có checkbox ở mỗi dòng (cho bulk actions)
  - Có nút "Xử lý xong" ở mỗi sự cố mới

#### 2.3. Xem Chi tiết và Comment
- [ ] Click vào dòng sự cố → Modal detail mở
- [ ] Vào tab "Bình luận"
- [ ] Thêm comment: "Tôi sẽ cử thợ đến sửa chiều nay"
- [ ] Kiểm tra badge "Chủ nhà" hiển thị
- [ ] Kiểm tra renter nhận notification

#### 2.4. Thay đổi Trạng thái
- [ ] Trong detail modal, tab "Thông tin"
- [ ] Thay đổi status từ "Mới" → "Đang xử lý"
- [ ] Click "Cập nhật trạng thái"
- [ ] **Kiểm tra:**
  - Modal refresh, status badge đổi màu xanh dương
  - Tab "Lịch sử" có record mới
  - Renter nhận notification

#### 2.5. Đánh dấu "Đã xử lý" (Quick Action)
- [ ] Đóng modal
- [ ] Click nút "Xử lý xong" ở dòng sự cố
- [ ] **Kiểm tra:**
  - Status chuyển thành "Chờ xác nhận" (badge màu xanh)
  - Nút "Xử lý xong" biến mất, thay bằng "Chờ xác nhận"
  - Renter nhận notification + email

#### 2.6. Test Bulk Actions
- [ ] Chọn 2-3 sự cố bằng checkbox
- [ ] Toolbar bulk actions xuất hiện
- [ ] Chọn status "Đang xử lý"
- [ ] Click "Cập nhật X"
- [ ] **Kiểm tra:**
  - Tất cả sự cố được chọn đổi status
  - Mỗi sự cố có record lịch sử
  - Renter nhận notification cho từng sự cố

---

### 3. Test Workflow Xác nhận (Renter Confirmation)

#### 3.1. Renter Xác nhận "Đã xong"
- [ ] Đăng nhập lại với tài khoản renter
- [ ] Vào "Sự cố" → Thấy sự cố có status "Chờ xác nhận"
- [ ] Click vào sự cố → Modal mở
- [ ] **Kiểm tra alert vàng hiển thị:**
  - "Chủ nhà đã đánh dấu đã xử lý xong"
  - Nút "Xác nhận đã xong" (xanh lá)
  - Nút "Chưa xong" (vàng)
- [ ] Click "Xác nhận đã xong"
- [ ] **Kiểm tra:**
  - Modal refresh
  - Status chuyển thành "Đã xử lý" (badge xanh lá)
  - Có timestamp "Thời gian xử lý xong"
  - Tab lịch sử có "Khách thuê xác nhận"
  - Landlord nhận notification

#### 3.2. Renter Từ chối "Chưa xong"
- [ ] Tạo sự cố mới (lặp lại bước 1.2)
- [ ] Chờ landlord đánh dấu "Đã xử lý"
- [ ] Renter vào detail modal
- [ ] Click nút "Chưa xong"
- [ ] Form mở ra với textarea
- [ ] Nhập lý do: "Điều hòa vẫn không lạnh, chỉ chạy quạt"
- [ ] Click "Gửi phản hồi"
- [ ] **Kiểm tra:**
  - Status chuyển thành "Chưa xong" (badge đỏ)
  - Lý do từ chối hiển thị trong lịch sử
  - Landlord nhận notification + email với lý do

---

### 4. Test Responsive và Mobile

#### 4.1. Desktop (>= 992px)
- [ ] Thu nhỏ cửa sổ browser xuống < 992px
- [ ] Navbar collapse thành hamburger menu (3 vạch)
- [ ] Click icon hamburger → Menu hiển thị
- [ ] **Kiểm tra:**
  - Menu có background màu tím
  - Tất cả text màu trắng (nhìn rõ)
  - Không có text trắng trên nền trắng

#### 4.2. Tablet và Mobile
- [ ] Test trên tablet (iPad)
- [ ] Test trên điện thoại (iPhone/Android)
- [ ] **Kiểm tra:**
  - Modal fit màn hình
  - Form nhập liệu dễ sử dụng
  - Tabs chuyển đổi mượt
  - Upload ảnh hoạt động

---

### 5. Test Email Notifications

#### 5.1. Cấu hình Email (Nếu chưa)
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

#### 5.2. Test Email
- [ ] Renter tạo sự cố → Landlord nhận email
- [ ] Landlord comment → Renter nhận email
- [ ] Landlord đổi status → Renter nhận email
- [ ] Landlord đánh dấu xong → Renter nhận email
- [ ] Renter từ chối → Landlord nhận email

---

### 6. Test Security và Authorization

#### 6.1. Renter Restrictions
- [ ] Đăng nhập renter
- [ ] Thử truy cập URL landlord: `/issues/` 
- [ ] **Kết quả:** Chuyển về trang index với message lỗi
- [ ] Thử resolve issue trực tiếp qua URL: `/issues/1/resolve/`
- [ ] **Kết quả:** 403 Forbidden

#### 6.2. Landlord Restrictions  
- [ ] Đăng nhập landlord
- [ ] Thử truy cập URL renter: `/renter/issues/`
- [ ] **Kết quả:** Chuyển về trang index với message lỗi
- [ ] Thử báo sự cố qua URL: `/issues/report/`
- [ ] **Kết quả:** Chuyển về dashboard với message lỗi

#### 6.3. Cross-user Access
- [ ] Renter A thử xác nhận issue của Renter B
- [ ] **Kết quả:** 403 Unauthorized
- [ ] Landlord A thử resolve issue của Landlord B
- [ ] **Kết quả:** 404 Not Found

---

### 7. Test Edge Cases

#### 7.1. Empty States
- [ ] Renter chưa có sự cố nào → Hiển thị "Chưa có sự cố"
- [ ] Issue chưa có comment → "Chưa có bình luận"
- [ ] Issue chưa có hình ảnh → "Chưa có hình ảnh"

#### 7.2. Validation
- [ ] Báo sự cố không chọn nhà → Hiển thị lỗi
- [ ] Báo sự cố không nhập tiêu đề → Hiển thị lỗi
- [ ] Comment trống → Button disable
- [ ] Upload file không phải ảnh → Hiển thị lỗi

#### 7.3. Long Content
- [ ] Nhập mô tả rất dài (>1000 ký tự) → Hiển thị đầy đủ
- [ ] Tiêu đề dài → Không bị vỡ layout
- [ ] Nhiều comments (>20) → Scroll trong modal

---

### 8. Test Performance

#### 8.1. HTMX và Real-time
- [ ] Badge notification update mỗi 10 giây
- [ ] Form submit không reload page
- [ ] Modal content load nhanh
- [ ] Comment append ngay lập tức

#### 8.2. Image Handling
- [ ] Upload ảnh lớn (>5MB) → Kiểm tra performance
- [ ] Upload nhiều ảnh cùng lúc → Tất cả được lưu
- [ ] Preview ảnh trước khi upload → Hiển thị nhanh

---

## ✅ Kết quả Mong đợi

Sau khi test xong tất cả checklist trên:

1. ✅ Renter có thể báo cáo, comment, xác nhận/từ chối sự cố
2. ✅ Landlord có thể xem, comment, thay đổi status, bulk update
3. ✅ Notification và email hoạt động đầy đủ
4. ✅ Security: Mỗi role chỉ truy cập được chức năng của mình
5. ✅ Responsive: Hoạt động tốt trên mọi thiết bị
6. ✅ UI/UX: Text luôn nhìn rõ, không có contrast issue
7. ✅ Performance: Mượt mà, không lag

---

## 🐛 Báo lỗi

Nếu phát hiện lỗi, ghi rõ:
- Bước nào trong checklist
- Tài khoản test (renter/landlord)
- Screenshot hoặc mô tả lỗi
- Browser và kích thước màn hình

---

**Ngày test:** ___________  
**Người test:** ___________  
**Kết quả:** ⬜ Pass / ⬜ Fail  
**Ghi chú:** _________________________
