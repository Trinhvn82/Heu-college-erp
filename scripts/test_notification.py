#!/usr/bin/env python
"""
Script to create test notifications
Usage: python test_notification.py <username>
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CollegeERP.settings')
django.setup()

from info.models import User
from sms.models import Notification

def create_test_notification(username):
    try:
        user = User.objects.get(username=username)
        
        # Create a test notification
        notif = Notification.objects.create(
            user=user,
            title="Thông báo kiểm tra",
            message="Đây là thông báo test để kiểm tra hệ thống notification.",
            type='bill_created',
            target_url='/'
        )
        
        print(f"✅ Created notification #{notif.id} for user: {username}")
        print(f"   Title: {notif.title}")
        print(f"   Unread notifications for {username}: {Notification.objects.filter(user=user, is_read=False).count()}")
        
    except User.DoesNotExist:
        print(f"❌ User '{username}' not found")
        print("\nAvailable users:")
        for u in User.objects.all()[:10]:
            print(f"  - {u.username}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test_notification.py <username>")
        print("\nAvailable users:")
        for u in User.objects.all()[:10]:
            print(f"  - {u.username}")
    else:
        create_test_notification(sys.argv[1])
