
## Recommended Static Structure

```
static/
├── css/
│   ├── vendor/                # Third-party libraries
│   │   ├── bootstrap/
│   │   └── animate/
│   ├── base.css              # Base styles (reset, variables)
│   ├── custom.css            # Global custom styles
│   ├── rental.css            # Rental management specific
│   └── dashboard.css         # Dashboard specific
│
├── js/
│   ├── vendor/               # Third-party libraries
│   │   ├── jquery/
│   │   ├── bootstrap/
│   │   └── htmx/
│   ├── core/                 # Core functionality
│   │   ├── utils.js
│   │   └── api.js
│   ├── components/           # Reusable components
│   │   ├── modal.js
│   │   ├── notifications.js
│   │   └── forms.js
│   └── pages/                # Page-specific
│       ├── dashboard.js
│       ├── bills.js
│       └── contracts.js
│
├── images/
│   ├── icons/                # App icons
│   ├── logos/                # Logos
│   ├── backgrounds/          # Background images
│   └── uploads/              # System images
│
├── fonts/                    # Custom fonts
│   ├── arial/
│   └── custom/
│
└── admin_interface/          # Django admin theme (keep separate)
```

## Actions to Take:

### 1. Remove Duplicates
- Run `python manage.py collectstatic` to consolidate
- Remove duplicate static folders from apps (sms/static, dashboard/static)
- Keep only app-specific static in app directories

### 2. Organize CSS
Current custom CSS files:
   - static\css\styles.css
   - static\static-rent\assets\animatecss\animate.css
   - static\static-rent\assets\dropdown\css\style.css
   - static\static-rent\assets\mobirise\css\mbr-additional.css
   - static\static-rent\assets\socicon\css\styles.css
   - static\static-rent\assets\theme\css\style.css
   - static\static-rent\assets\web\assets\mobirise-icons2\mobirise2.css
   - static\static-rent\css\style.css
   - sms\static\assets\css\volt.css
   - sms\static\css\landing-custom.css
   - sms\static\css\modals.css
   - sms\static\css\styles.css
   - sms\static\dist\css\style.css
   - sms\static\dist\css\style.min.css
   - sms\static\info\homepage\css\heroic-features.css
   - sms\static\rest_framework\css\default.css
   - sms\static\rest_framework\css\font-awesome-4.0.3.css
   - sms\static\rest_framework\css\prettify.css
   - sms\static\rest_framework\docs\css\base.css
   - sms\static\rest_framework\docs\css\highlight.css
   - sms\static\rest_framework\docs\css\jquery.json-view.min.css
   - sms\static\src\css\style.css
   - sms\static\src\css\style.min.css
   - sms\static\static-rent\assets\animatecss\animate.css
   - sms\static\static-rent\assets\dropdown\css\style.css
   - sms\static\static-rent\assets\mobirise\css\mbr-additional.css
   - sms\static\static-rent\assets\socicon\css\styles.css
   - sms\static\static-rent\assets\theme\css\style.css
   - sms\static\static-rent\assets\web\assets\mobirise-icons2\mobirise2.css
   - sms\static\static-rent\css\style.css
   - dashboard\static\dist\css\style.css
   - dashboard\static\dist\css\style.min.css
   - dashboard\static\info\homepage\css\heroic-features.css
   - dashboard\static\rest_framework\css\default.css
   - dashboard\static\rest_framework\css\font-awesome-4.0.3.css
   - dashboard\static\rest_framework\css\prettify.css
   - dashboard\static\rest_framework\docs\css\base.css
   - dashboard\static\rest_framework\docs\css\highlight.css
   - dashboard\static\rest_framework\docs\css\jquery.json-view.min.css
   - dashboard\static\src\css\headers.css
   - dashboard\static\src\css\sidebars.css
   - dashboard\static\src\css\style.css
   - dashboard\static\src\css\style.min.css
   - info\static\info\homepage\css\heroic-features.css
   - htmx_patterns\static\css\modals.css
   - htmx_patterns\static\css\pure_base.css

Action:
   → Consolidate into static/css/custom.css
   → Create static/css/rental.css for rental-specific styles
   → Move vendor CSS to static/css/vendor/

### 3. Organize JavaScript
Current custom JS files need organization.

Action:
   → Move reusable code to static/js/core/
   → Move component code to static/js/components/
   → Move page-specific code to static/js/pages/
   → Move vendor JS to static/js/vendor/

### 4. Clean Up Images
Action:
   → Organize by type: icons/, logos/, backgrounds/
   → Remove unused images
   → Optimize large images (compress)

### 5. Remove Obsolete Static
Directories to review:
   - static-rent/ (appears to be old theme)
   - Duplicate admin/ directories

## Django Settings Check

Ensure settings.py has:

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For collectstatic
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

## Commands to Run

```bash
# 1. Collect all static files
python manage.py collectstatic --clear

# 2. Find unused static files
python manage.py findstatic <filename>

# 3. Test the application
python manage.py runserver
```

## Benefits

✅ Easier to maintain
✅ Faster to find files
✅ Better version control
✅ Clearer dependencies
✅ Improved performance
