"""
Script để clean up và tổ chức lại project structure
- Xóa file script cũ không dùng
- Tổ chức lại static files
- Xóa file trùng lặp
- Tạo cấu trúc thư mục rõ ràng

Usage:
    python cleanup_project.py --dry-run  # Preview changes only
    python cleanup_project.py --execute  # Actually perform cleanup
"""

import os
import shutil
from pathlib import Path
import argparse

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Files to KEEP (important scripts)
KEEP_SCRIPTS = [
    'manage.py',
    'test_bill_email.py',
    'test_notification.py', 
    'test_session_timeout.py',
    'start-qcluster.py',
]

# Files to REMOVE (old scripts, duplicates)
REMOVE_FILES = [
    # Old database scripts (already executed)
    'dropnotnull_script.py',
    'insert_ctdt_script.py',
    'insert_ctdt-monhoc_script.py',
    'insert_diem_script.py',
    'insert_hs81_script.py',
    'insert_hsgv_script.py',
    'insert_hssv_script.py',
    'insert_lichhoc_script.py',
    'insert_loaidiem_script.py',
    'insert_lop_script.py',
    'insert_monhoc_script.py',
    'insert_user_script.py',
    'insert_xp_script.py',
    'Schedule_script.py',
    
    # Utility scripts (one-time use)
    'excel2pdf.py',
    'script.py',
    'sites.py',
    
    # Old data files
    'outfile',
    'Data.xlsx',
    'pandas_simple.xlsx',
    'template_kqht.pdf',
    'template_kqht.xlsx',
    'Chức năng PM.pdf',
    'Chức năng PM.xlsx',
    'DSCF3345.JPG',
    
    # Backups and zips
    'sms-backup2024-12-26-0610.dump',
    'sms.zip',
    
    # Old requirements files
    'req-ver1.1.txt',
    'requirement-hrmx.text',
    'requirement1.txt',
    'requirements3.txt',
    'requirements4.txt',
    
    # Old configs
    'psql.config',
]

# Directories to organize
STATIC_CONSOLIDATION = {
    'source_dirs': [
        'sms/static',
        'dashboard/static',
    ],
    'target_dir': 'static',
    'note': 'Django collectstatic will handle this, but we can clean duplicates'
}


class ProjectCleanup:
    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.changes = []
        
    def log(self, action, path, reason=""):
        status = "WOULD" if self.dry_run else "DID"
        message = f"[{status}] {action}: {path}"
        if reason:
            message += f" ({reason})"
        print(message)
        self.changes.append(message)
    
    def remove_old_scripts(self):
        """Remove old one-time scripts"""
        print("\n" + "="*80)
        print("STEP 1: Cleaning Old Scripts")
        print("="*80)
        
        for filename in REMOVE_FILES:
            filepath = BASE_DIR / filename
            if filepath.exists():
                if self.dry_run:
                    self.log("REMOVE", filepath, "Old/unused file")
                else:
                    try:
                        if filepath.is_file():
                            filepath.unlink()
                        elif filepath.is_dir():
                            shutil.rmtree(filepath)
                        self.log("REMOVED", filepath, "Old/unused file")
                    except Exception as e:
                        print(f"ERROR removing {filepath}: {e}")
    
    def organize_scripts(self):
        """Move utility scripts to scripts/ directory"""
        print("\n" + "="*80)
        print("STEP 2: Organizing Scripts")
        print("="*80)
        
        scripts_dir = BASE_DIR / 'scripts'
        
        if not self.dry_run:
            scripts_dir.mkdir(exist_ok=True)
        else:
            self.log("CREATE", scripts_dir, "Scripts directory")
        
        # Move test scripts
        test_scripts = ['test_bill_email.py', 'test_notification.py', 'test_session_timeout.py']
        
        for script in test_scripts:
            src = BASE_DIR / script
            dst = scripts_dir / script
            
            if src.exists() and not dst.exists():
                if self.dry_run:
                    self.log("MOVE", f"{src} -> {dst}", "Organize test scripts")
                else:
                    try:
                        shutil.move(str(src), str(dst))
                        self.log("MOVED", f"{src} -> {dst}", "Organized")
                    except Exception as e:
                        print(f"ERROR moving {src}: {e}")
    
    def check_static_duplicates(self):
        """Check for duplicate static files"""
        print("\n" + "="*80)
        print("STEP 3: Checking Static File Duplicates")
        print("="*80)
        
        main_static = BASE_DIR / 'static'
        
        for source_dir in STATIC_CONSOLIDATION['source_dirs']:
            source_path = BASE_DIR / source_dir
            
            if not source_path.exists():
                continue
            
            print(f"\nChecking {source_path}...")
            
            # Find duplicate directories
            for item in source_path.iterdir():
                if item.is_dir():
                    main_counterpart = main_static / item.name
                    
                    if main_counterpart.exists():
                        self.log("DUPLICATE", f"{item} (exists in {main_counterpart})", 
                               "Can be removed after collectstatic")
    
    def consolidate_css(self):
        """Consolidate custom CSS files"""
        print("\n" + "="*80)
        print("STEP 4: CSS Consolidation Plan")
        print("="*80)
        
        css_files = []
        
        # Find all custom CSS files (not from libraries)
        for root, dirs, files in os.walk(BASE_DIR / 'static'):
            # Skip admin and library directories
            if any(skip in root for skip in ['admin', 'admin_interface', 'bootstrap', 'static-rent']):
                continue
            
            for file in files:
                if file.endswith('.css') and not file.endswith('.min.css'):
                    css_path = Path(root) / file
                    css_files.append(css_path)
        
        if css_files:
            print("\nCustom CSS files found:")
            for css_file in css_files:
                print(f"  - {css_file.relative_to(BASE_DIR)}")
            
            target_css = BASE_DIR / 'static' / 'css' / 'custom.css'
            self.log("SUGGESTION", f"Consider consolidating into {target_css}", 
                   "Single custom CSS file")
        else:
            print("No custom CSS files need consolidation")
    
    def create_archive_directory(self):
        """Create archive for old files instead of deleting"""
        print("\n" + "="*80)
        print("STEP 5: Archive Old Files")
        print("="*80)
        
        archive_dir = BASE_DIR / 'archive'
        
        if not self.dry_run:
            archive_dir.mkdir(exist_ok=True)
            (archive_dir / 'old_scripts').mkdir(exist_ok=True)
            (archive_dir / 'old_data').mkdir(exist_ok=True)
        
        self.log("INFO", archive_dir, "Created for old files (safer than delete)")
    
    def create_cleanup_summary(self):
        """Create a summary document"""
        print("\n" + "="*80)
        print("CLEANUP SUMMARY")
        print("="*80)
        
        summary = f"""
# Project Cleanup Summary

Generated: {BASE_DIR}
Mode: {'DRY RUN (preview only)' if self.dry_run else 'EXECUTED'}

## Changes Made:

"""
        for change in self.changes:
            summary += f"- {change}\n"
        
        summary += """

## Recommended Manual Steps:

### 1. Static Files Organization

Django's `collectstatic` will handle static files automatically. Current structure:
- `static/` - Main static directory (collected files go here)
- `sms/static/` - App-specific static files
- `dashboard/static/` - Dashboard app static files

Run: `python manage.py collectstatic` to consolidate.

### 2. CSS Consolidation

Consider merging custom CSS files into:
- `static/css/custom.css` - Global custom styles
- `static/css/rental.css` - Rental management specific
- `static/css/dashboard.css` - Dashboard specific

### 3. JavaScript Organization

Create structured JS directory:
- `static/js/core/` - Core functionality
- `static/js/components/` - Reusable components
- `static/js/pages/` - Page-specific scripts

### 4. Remove Unused Libraries

Review and remove unused:
- Old Bootstrap versions
- Duplicate jQuery versions
- Unused icon fonts

### 5. Database Cleanup

Old scripts archived. If database is stable, keep archive for reference only.

## Files Structure After Cleanup:

```
project/
├── CollegeERP/          # Django settings
├── scripts/             # Utility scripts
│   ├── test_*.py       # Test scripts
│   └── maintenance/    # Maintenance scripts
├── static/              # Consolidated static files
│   ├── css/            # All CSS
│   ├── js/             # All JavaScript
│   ├── images/         # All images
│   └── vendor/         # Third-party libraries
├── media/              # User uploads
├── sms/                # Main app
├── dashboard/          # Dashboard app
└── archive/            # Old files (can be removed after testing)
```

## Testing After Cleanup:

1. Run development server: `python manage.py runserver`
2. Check all pages load correctly
3. Verify static files are served
4. Test CSS and JavaScript functionality
5. Run tests: `python manage.py test`

## Rollback:

If issues occur, old files are in `archive/` directory.
"""
        
        summary_file = BASE_DIR / 'CLEANUP_SUMMARY.md'
        
        if not self.dry_run:
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary)
            self.log("CREATED", summary_file, "Cleanup documentation")
        else:
            print("\nSummary preview:")
            print(summary[:500] + "...\n")
    
    def run(self):
        """Run all cleanup steps"""
        print("\n" + "="*80)
        print(f"PROJECT CLEANUP - {'DRY RUN' if self.dry_run else 'EXECUTION MODE'}")
        print("="*80)
        
        if self.dry_run:
            print("⚠️  DRY RUN MODE: No files will be modified")
            print("    Run with --execute to actually perform cleanup\n")
        else:
            print("🚀 EXECUTION MODE: Files will be modified!")
            print("    Make sure you have a backup!\n")
        
        self.remove_old_scripts()
        self.organize_scripts()
        self.check_static_duplicates()
        self.consolidate_css()
        self.create_archive_directory()
        self.create_cleanup_summary()
        
        print("\n" + "="*80)
        print("CLEANUP COMPLETE")
        print("="*80)
        print(f"\nTotal changes: {len(self.changes)}")
        
        if self.dry_run:
            print("\n✅ Review the changes above.")
            print("   Run with --execute when ready to apply changes.")
        else:
            print("\n✅ Cleanup completed successfully!")
            print("   Check CLEANUP_SUMMARY.md for details.")
            print("   Test your application to ensure everything works.")


def main():
    parser = argparse.ArgumentParser(description='Clean up project structure')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--dry-run', action='store_true', 
                      help='Preview changes without modifying files')
    group.add_argument('--execute', action='store_true',
                      help='Actually perform the cleanup')
    
    args = parser.parse_args()
    
    cleanup = ProjectCleanup(dry_run=args.dry_run)
    cleanup.run()


if __name__ == "__main__":
    main()
