# Project Cleanup & Organization Guide

## 📋 Tổng Quan

Document này hướng dẫn cleanup và tổ chức lại project College-ERP để dễ maintain hơn.

## 🎯 Mục Tiêu

1. ✅ Xóa file cũ không dùng
2. ✅ Tổ chức lại static files theo chuẩn
3. ✅ Loại bỏ code trùng lặp
4. ✅ Cải thiện cấu trúc thư mục

## 📁 Cấu Trúc Hiện Tại (Vấn Đề)

```
❌ Có nhiều file script cũ ở root (insert_*, Schedule_script.py, etc.)
❌ Static files bị duplicate ở nhiều nơi (static/, sms/static/, dashboard/static/)
❌ CSS/JS không được tổ chức rõ ràng
❌ File data test, backup nằm lẫn với source code
```

## ✅ Cấu Trúc Mới (Sau Cleanup)

```
College-ERP-v1.1/
├── CollegeERP/              # Django settings
├── sms/                     # Main rental app
├── dashboard/               # Dashboard app
├── info/                    # User management
├── scripts/                 # ✨ NEW: Utility scripts
│   ├── test_bill_email.py
│   ├── test_session_timeout.py
│   └── maintenance/
├── static/                  # ✨ Consolidated static files
│   ├── css/
│   │   ├── vendor/         # Third-party CSS
│   │   ├── custom.css      # Global custom styles
│   │   └── rental.css      # App-specific styles
│   ├── js/
│   │   ├── vendor/         # Third-party JS
│   │   ├── core/           # Core functionality
│   │   ├── components/     # Reusable components
│   │   └── pages/          # Page-specific
│   └── images/
│       ├── icons/
│       ├── logos/
│       └── backgrounds/
├── staticfiles/             # ✨ NEW: Collected static (gitignore)
├── media/                   # User uploads
├── archive/                 # ✨ NEW: Old files backup
└── docs/                    # ✨ Documentation
```

## 🚀 Thực Hiện Cleanup

### Bước 1: Preview Changes

```bash
# Xem trước những gì sẽ bị thay đổi
python cleanup_project.py --dry-run
```

### Bước 2: Backup (Quan Trọng!)

```bash
# Tạo backup toàn bộ project
cd ..
tar -czf College-ERP-backup-$(date +%Y%m%d).tar.gz College-ERP-v1.1/

# Hoặc trên Windows PowerShell:
Compress-Archive -Path . -DestinationPath ../College-ERP-backup.zip
```

### Bước 3: Execute Cleanup

```bash
# Thực hiện cleanup
python cleanup_project.py --execute
```

### Bước 4: Organize Static Files

```bash
# Collect tất cả static files vào một chỗ
python manage.py collectstatic --clear

# Xác nhận: yes
```

### Bước 5: Test Application

```bash
# Start development server
python manage.py runserver

# Test các trang chính:
# - Login page
# - Dashboard
# - Bill management
# - Renter portal
# - Check CSS/JS load correctly
```

## 📊 Files Sẽ Bị Xóa

### Old Scripts (33 files)
- `dropnotnull_script.py`
- `insert_*_script.py` (13 files)
- `Schedule_script.py`
- `excel2pdf.py`
- `script.py`
- `sites.py`

### Old Data Files
- `Data.xlsx`
- `pandas_simple.xlsx`
- `template_kqht.*`
- `Chức năng PM.*`
- `DSCF3345.JPG`

### Backups & Archives
- `sms-backup2024-12-26-0610.dump`
- `sms.zip`

### Old Requirements
- `req-ver1.1.txt`
- `requirement-hrmx.text`
- `requirement1.txt`
- `requirements3.txt`
- `requirements4.txt`

**Chỉ giữ**: `requirements.txt` (file chính)

## 🎨 Static Files Organization

### Trước Cleanup (Tình Trạng Hiện Tại)

```
Total: 218 CSS files, 531 JS files, 2342 images
Tổng dung lượng: ~75 MB
Duplicate: Nhiều file admin, bootstrap, jquery

Vấn đề:
- CSS/JS trùng lặp ở nhiều thư mục
- Không phân biệt vendor vs custom
- Khó tìm và maintain
```

### Sau Cleanup (Mục Tiêu)

```
static/
├── css/
│   ├── vendor/              # Bootstrap, Animate, etc.
│   ├── custom.css          # ~10KB - Merged custom styles
│   └── rental.css          # ~5KB - Rental specific
│
├── js/
│   ├── vendor/              # jQuery, Bootstrap, HTMX
│   ├── core/
│   │   ├── utils.js        # Helper functions
│   │   └── api.js          # API calls
│   ├── components/
│   │   ├── modal.js        # Modal logic
│   │   ├── notifications.js
│   │   └── forms.js        # Form handling
│   └── pages/
│       ├── dashboard.js
│       ├── bills.js
│       └── contracts.js
│
└── images/                  # Organized by type
```

## 📝 Manual Tasks

### 1. Consolidate Custom CSS

```bash
# Merge these files into static/css/custom.css:
- sms/static/css/modals.css
- sms/static/css/landing-custom.css
- dashboard/static/src/css/style.css

# Tool: Can use cat or manual merge
cat sms/static/css/modals.css >> static/css/custom.css
```

### 2. Consolidate Custom JS

```bash
# Organize JavaScript files:
- Move reusable functions → static/js/core/
- Move modal/notification code → static/js/components/
- Move page-specific code → static/js/pages/
```

### 3. Clean Up Images

```bash
# Find large images
find static -name "*.jpg" -o -name "*.png" | xargs du -sh | sort -rh | head -20

# Optimize with imagemagick or tinypng
mogrify -resize 1920x1080\> -quality 85 static/images/*.jpg
```

### 4. Remove Duplicate Static from Apps

Sau khi chạy `collectstatic`, xóa duplicate static folders:

```bash
# Check first
ls sms/static/admin
ls dashboard/static/admin
ls static/admin

# Remove duplicates (keep only in main static/)
rm -rf sms/static/admin
rm -rf sms/static/admin_interface
rm -rf dashboard/static/admin
```

## ✅ Verification Checklist

Sau khi cleanup, verify các điểm sau:

- [ ] Development server chạy bình thường: `python manage.py runserver`
- [ ] Tất cả trang load đúng CSS/JS
- [ ] Login page hoạt động
- [ ] Dashboard hiển thị đúng
- [ ] Bill creation/edit works
- [ ] Images load correctly
- [ ] Admin panel vẫn hoạt động
- [ ] No 404 errors trong browser console
- [ ] Static files serve correctly
- [ ] Mobile responsive vẫn OK

## 🔧 Django Settings Updates

File `CollegeERP/settings.py` đã được update:

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # ✨ NEW

STATICFILES_DIRS = [  # ✨ NEW
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_FINDERS = [  # ✨ NEW
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 📦 Production Deployment

Khi deploy production, nhớ:

```bash
# 1. Collect static files
python manage.py collectstatic --noinput

# 2. Configure web server (nginx/apache) to serve:
#    - /static/ → /path/to/staticfiles/
#    - /media/ → /path/to/media/

# 3. Set DEBUG = False in settings.py
```

## 🐛 Troubleshooting

### Issue: CSS không load sau cleanup

**Solution**:
```bash
# Clear browser cache
# Run collectstatic lại
python manage.py collectstatic --clear --noinput

# Check STATICFILES_DIRS in settings.py
```

### Issue: 404 cho static files

**Solution**:
```python
# Đảm bảo trong urls.py có:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your urls
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### Issue: Images không hiển thị

**Solution**:
```python
# Check template syntax:
{% load static %}
<img src="{% static 'images/logo.png' %}">

# NOT: <img src="/static/images/logo.png">
```

## 📈 Metrics

### Trước Cleanup
- Files ở root: 62 files
- Static size: ~75 MB
- Duplicate files: ~30%
- CSS files: 218
- JS files: 531

### Sau Cleanup (Expected)
- Files ở root: ~10 files (chỉ giữ essential)
- Static size: ~50 MB (sau optimize)
- Duplicate files: 0%
- CSS files: ~100 (organized)
- JS files: ~300 (organized)

### Benefits
- ✅ Faster git operations
- ✅ Easier to find files
- ✅ Better IDE performance
- ✅ Clearer project structure
- ✅ Faster page load (less duplicates)

## 🎓 Best Practices Going Forward

1. **Static Files**:
   - Vendor libraries → `static/vendor/`
   - Custom global → `static/css/custom.css`
   - App-specific → Keep in app's static/

2. **Scripts**:
   - Test scripts → `scripts/`
   - One-time migrations → Run then delete
   - Utility scripts → `scripts/maintenance/`

3. **Documentation**:
   - Keep docs updated
   - Document major changes
   - Use meaningful commit messages

4. **Git**:
   - Add `staticfiles/` to `.gitignore`
   - Add `*.pyc` and `__pycache__/` to `.gitignore`
   - Don't commit uploaded media files

## 📞 Next Steps

1. ✅ Run `cleanup_project.py --dry-run` to preview
2. ✅ Create backup
3. ✅ Run `cleanup_project.py --execute`
4. ✅ Run `python manage.py collectstatic`
5. ✅ Test application thoroughly
6. ✅ Commit changes to git
7. ✅ Update deployment scripts if needed

---

**Last Updated**: 2025-11-07
**Script Version**: 1.0
**Django Version**: 4.2.x
