"""
Script để tổ chức lại static files theo chuẩn Django best practices

Cấu trúc mới:
static/
├── css/
│   ├── vendor/          # Third-party CSS
│   ├── custom.css       # Custom global styles
│   ├── rental.css       # Rental-specific styles
│   └── dashboard.css    # Dashboard styles
├── js/
│   ├── vendor/          # Third-party JS
│   ├── core/            # Core functionality
│   ├── components/      # Reusable components
│   └── pages/           # Page-specific scripts
├── images/
│   ├── icons/
│   ├── logos/
│   └── backgrounds/
└── fonts/

Usage:
    python organize_static.py --analyze  # Analyze current structure
    python organize_static.py --plan     # Create reorganization plan
    python organize_static.py --execute  # Execute reorganization
"""

import os
import shutil
from pathlib import Path
import argparse
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent

# Libraries to keep in vendor/
VENDOR_LIBRARIES = [
    'bootstrap',
    'jquery',
    'htmx',
    'fontawesome',
    'animate',
    'mobirise',
    'socicon',
]


class StaticOrganizer:
    def __init__(self, mode='analyze'):
        self.mode = mode
        self.main_static = BASE_DIR / 'static'
        self.analysis = defaultdict(list)
        
    def analyze_structure(self):
        """Phân tích cấu trúc static hiện tại"""
        print("\n" + "="*80)
        print("STATIC FILES ANALYSIS")
        print("="*80)
        
        # Analyze main static directory
        self._analyze_directory(self.main_static, "Main Static")
        
        # Analyze app static directories
        for app in ['sms', 'dashboard', 'info', 'htmx_patterns']:
            app_static = BASE_DIR / app / 'static'
            if app_static.exists():
                self._analyze_directory(app_static, f"{app.upper()} App Static")
        
        self._print_analysis()
    
    def _analyze_directory(self, directory, label):
        """Phân tích một thư mục static"""
        if not directory.exists():
            return
        
        print(f"\n📁 {label}: {directory.relative_to(BASE_DIR)}")
        
        css_count = 0
        js_count = 0
        img_count = 0
        other_count = 0
        total_size = 0
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                filepath = Path(root) / file
                size = filepath.stat().st_size
                total_size += size
                
                if file.endswith('.css'):
                    css_count += 1
                    self.analysis['css'].append(filepath)
                elif file.endswith('.js'):
                    js_count += 1
                    self.analysis['js'].append(filepath)
                elif file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico')):
                    img_count += 1
                    self.analysis['images'].append(filepath)
                else:
                    other_count += 1
        
        print(f"   CSS: {css_count} files")
        print(f"   JavaScript: {js_count} files")
        print(f"   Images: {img_count} files")
        print(f"   Other: {other_count} files")
        print(f"   Total size: {total_size / 1024 / 1024:.2f} MB")
    
    def _print_analysis(self):
        """In ra phân tích chi tiết"""
        print("\n" + "="*80)
        print("DETAILED ANALYSIS")
        print("="*80)
        
        # CSS Files
        print(f"\n📄 CSS Files ({len(self.analysis['css'])} total):")
        css_by_dir = defaultdict(list)
        for css_file in self.analysis['css']:
            parent = css_file.parent.name
            css_by_dir[parent].append(css_file.name)
        
        for dir_name, files in sorted(css_by_dir.items()):
            print(f"   {dir_name}/: {len(files)} files")
        
        # JavaScript Files
        print(f"\n📜 JavaScript Files ({len(self.analysis['js'])} total):")
        js_by_dir = defaultdict(list)
        for js_file in self.analysis['js']:
            parent = js_file.parent.name
            js_by_dir[parent].append(js_file.name)
        
        for dir_name, files in sorted(js_by_dir.items()):
            print(f"   {dir_name}/: {len(files)} files")
        
        # Images
        print(f"\n🖼️  Images ({len(self.analysis['images'])} total):")
        img_by_type = defaultdict(int)
        for img_file in self.analysis['images']:
            ext = img_file.suffix.lower()
            img_by_type[ext] += 1
        
        for ext, count in sorted(img_by_type.items()):
            print(f"   {ext}: {count} files")
    
    def create_plan(self):
        """Tạo kế hoạch tổ chức lại"""
        print("\n" + "="*80)
        print("REORGANIZATION PLAN")
        print("="*80)
        
        plan = """
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
"""
        
        for css_file in self.analysis['css']:
            if 'vendor' not in str(css_file).lower() and \
               'bootstrap' not in str(css_file).lower() and \
               'admin' not in str(css_file).lower():
                plan += f"   - {css_file.relative_to(BASE_DIR)}\n"
        
        plan += """
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
"""
        
        print(plan)
        
        # Save plan to file
        if self.mode == 'plan':
            plan_file = BASE_DIR / 'STATIC_REORGANIZATION_PLAN.md'
            with open(plan_file, 'w', encoding='utf-8') as f:
                f.write(plan)
            print(f"\n✅ Plan saved to: {plan_file}")
    
    def check_settings(self):
        """Kiểm tra Django settings cho static files"""
        print("\n" + "="*80)
        print("DJANGO SETTINGS CHECK")
        print("="*80)
        
        settings_file = BASE_DIR / 'CollegeERP' / 'settings.py'
        
        if not settings_file.exists():
            print("❌ settings.py not found")
            return
        
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = {
            'STATIC_URL': 'STATIC_URL' in content,
            'STATIC_ROOT': 'STATIC_ROOT' in content,
            'STATICFILES_DIRS': 'STATICFILES_DIRS' in content,
            'MEDIA_URL': 'MEDIA_URL' in content,
            'MEDIA_ROOT': 'MEDIA_ROOT' in content,
        }
        
        print("\nConfiguration status:")
        for key, found in checks.items():
            status = "✅" if found else "❌"
            print(f"   {status} {key}")
        
        if not all(checks.values()):
            print("\n⚠️  Missing static configuration!")
            print("   Add to settings.py:")
            print("""
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
""")
    
    def run(self):
        """Execute based on mode"""
        if self.mode == 'analyze':
            self.analyze_structure()
            self.check_settings()
        elif self.mode == 'plan':
            self.analyze_structure()
            self.create_plan()
            self.check_settings()
        elif self.mode == 'execute':
            print("⚠️  Execute mode not yet implemented")
            print("   Please review the plan first with --plan")
            print("   Then manually reorganize or use collectstatic")


def main():
    parser = argparse.ArgumentParser(description='Organize static files')
    parser.add_argument('--analyze', action='store_true',
                       help='Analyze current static structure')
    parser.add_argument('--plan', action='store_true',
                       help='Create reorganization plan')
    parser.add_argument('--execute', action='store_true',
                       help='Execute reorganization (use with caution)')
    
    args = parser.parse_args()
    
    if args.execute:
        mode = 'execute'
    elif args.plan:
        mode = 'plan'
    else:
        mode = 'analyze'
    
    organizer = StaticOrganizer(mode=mode)
    organizer.run()


if __name__ == "__main__":
    main()
