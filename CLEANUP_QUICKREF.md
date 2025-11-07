# Quick Cleanup Reference

## 🚀 Quick Start

```bash
# 1. Preview cleanup
python cleanup_project.py --dry-run

# 2. Create backup
Compress-Archive -Path . -DestinationPath ../backup.zip

# 3. Execute cleanup
python cleanup_project.py --execute

# 4. Collect static files
python manage.py collectstatic --clear

# 5. Test
python manage.py runserver
```

## 📁 What Gets Cleaned

### Removed (33 files)
- ❌ Old scripts: `insert_*.py`, `Schedule_script.py`
- ❌ Old data: `Data.xlsx`, `pandas_simple.xlsx`
- ❌ Backups: `*.dump`, `sms.zip`
- ❌ Old requirements: `requirement*.txt` (except main)

### Moved
- 📦 Test scripts → `scripts/`
- 📦 Old files → `archive/` (safe backup)

### Organized
- 🎨 Static files consolidated
- 📝 Documentation in one place

## 🎨 Static Files After Cleanup

```
static/
├── css/
│   ├── vendor/          # Bootstrap, etc.
│   ├── custom.css       # Your styles
│   └── rental.css       # App specific
├── js/
│   ├── vendor/          # jQuery, HTMX
│   ├── core/            # Utils
│   ├── components/      # Modals, forms
│   └── pages/           # Page specific
└── images/
    ├── icons/
    ├── logos/
    └── backgrounds/
```

## ✅ Verify After Cleanup

```bash
# Server runs
python manage.py runserver

# No errors in console
# All pages load CSS/JS
# Images display
# Forms work
```

## 🐛 If Something Breaks

```bash
# Restore from backup
cd ..
unzip backup.zip

# Or check archive/
ls archive/old_scripts/
```

## 📊 Before vs After

| Metric | Before | After |
|--------|--------|-------|
| Root files | 62 | ~15 |
| Static size | 75 MB | ~50 MB |
| Duplicates | 30% | 0% |
| Structure | Messy | Clean |

## 🎯 Commands Reference

```bash
# Analyze static
python organize_static.py --analyze

# Create plan
python organize_static.py --plan

# Check sessions
python manage.py check_sessions

# Test email
python scripts/test_bill_email.py <bill_id>

# Collectstatic
python manage.py collectstatic --clear --noinput
```

## 📝 Settings Updates

```python
# CollegeERP/settings.py - Already updated
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

## 🔗 Documentation

- 📖 Full guide: `CLEANUP_GUIDE.md`
- 📋 Static plan: `STATIC_REORGANIZATION_PLAN.md`
- 🔐 Session timeout: `SESSION_TIMEOUT_GUIDE.md`

---
**Quick Help**: If stuck, check CLEANUP_GUIDE.md for details
