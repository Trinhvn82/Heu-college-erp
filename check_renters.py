import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CollegeERP.settings')
django.setup()

from sms.models import Renter
from django.contrib.auth.models import User

print("=== Checking Renters ===")
renters = Renter.objects.all().order_by('id')
for r in renters:
    print(f"ID: {r.id:3d} | MA: {r.ma or 'None':10s} | Chu_ID: {r.chu_id or 'None'} | Name: {r.hoten}")

print("\n=== Checking Users (Landlords) ===")
users = User.objects.filter(is_superuser=False).order_by('id')[:10]
for u in users:
    print(f"User ID: {u.id:3d} | Username: {u.username:20s} | Name: {u.get_full_name()}")
