"""
Demo implementation script - Shows how to migrate URLs to use encoded IDs

This script demonstrates:
1. How to update urls.py
2. How to update views (minimal changes)
3. How to update templates
4. Testing encode/decode

Run: python demo_url_encoding.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CollegeERP.settings')
django.setup()

from sms.utils.id_encoder import encode_id, decode_id, encode_multiple, decode_multiple


def demo_basic_encoding():
    """Demo basic encode/decode"""
    print("\n" + "="*80)
    print("DEMO 1: Basic Encoding/Decoding")
    print("="*80)
    
    # Example IDs from database
    test_ids = [1, 10, 123, 456, 1000, 9999]
    
    print("\nInteger ID → Encoded Hash:")
    print("-" * 40)
    for id_num in test_ids:
        encoded = encode_id(id_num)
        print(f"  {id_num:6d} → {encoded}")
    
    print("\nEncoded Hash → Integer ID:")
    print("-" * 40)
    encoded_samples = [encode_id(id_num) for id_num in test_ids]
    for encoded in encoded_samples:
        decoded = decode_id(encoded)
        print(f"  {encoded:12s} → {decoded}")


def demo_url_examples():
    """Demo URL transformation"""
    print("\n" + "="*80)
    print("DEMO 2: URL Transformation Examples")
    print("="*80)
    
    examples = [
        ("Bill Detail", 123, "/sms/bill/{}/detail/"),
        ("Bill PDF", 456, "/sms/bill/{}/pdf/"),
        ("Payment Confirm", 789, "/sms/payment/confirm/{}/"),
        ("Issue Detail", 42, "/sms/issues/{}/"),
        ("Notification Read", 99, "/sms/notifications/{}/read/"),
        ("House Bills", 15, "/sms/location/{}/bills/"),
    ]
    
    print("\nBEFORE (Integer IDs - Insecure):")
    print("-" * 80)
    for name, id_num, pattern in examples:
        url = pattern.format(id_num)
        print(f"  {name:20s}: {url}")
    
    print("\nAFTER (Encoded IDs - Secure):")
    print("-" * 80)
    for name, id_num, pattern in examples:
        encoded = encode_id(id_num)
        url = pattern.format(encoded)
        print(f"  {name:20s}: {url}")


def demo_multiple_ids():
    """Demo encoding multiple IDs in one hash"""
    print("\n" + "="*80)
    print("DEMO 3: Multiple IDs in Single Hash")
    print("="*80)
    
    print("\nUse case: URL with multiple parameters")
    print("-" * 40)
    
    # Example: Import grades for a class and subject
    lop_id = 123
    lmh_id = 456
    ld_id = 789
    
    # Old way: separate parameters
    old_url = f"/sms/import_diemtp/{lop_id}/{lmh_id}/{ld_id}/"
    print(f"OLD URL: {old_url}")
    
    # New way: single hash
    hash_str = encode_multiple(lop_id, lmh_id, ld_id)
    new_url = f"/sms/import_diemtp/{hash_str}/"
    print(f"NEW URL: {new_url}")
    
    # Decode
    decoded = decode_multiple(hash_str)
    print(f"\nDecoded: {decoded}")
    print(f"  lop_id = {decoded[0]}")
    print(f"  lmh_id = {decoded[1]}")
    print(f"  ld_id = {decoded[2]}")


def demo_template_usage():
    """Demo template filter usage"""
    print("\n" + "="*80)
    print("DEMO 4: Template Usage Examples")
    print("="*80)
    
    print("\nExample 1: Simple link with filter")
    print("-" * 40)
    print("BEFORE:")
    print('''  <a href="{% url 'bill_detail' bill_id=bill.id %}">View Bill</a>''')
    print("\nAFTER:")
    print('''  {% load id_encoder %}''')
    print('''  <a href="{% url 'bill_detail' bill_id=bill.id|encode_id %}">View Bill</a>''')
    
    print("\n\nExample 2: Display encoded ID")
    print("-" * 40)
    print("BEFORE:")
    print('''  <p>Bill #{{ bill.id }}</p>  <!-- Shows: Bill #123 -->''')
    print("\nAFTER:")
    print('''  {% load id_encoder %}''')
    print('''  <p>Bill #{{ bill.id|encode_id }}</p>  <!-- Shows: Bill #jR7qKm3p -->''')
    
    print("\n\nExample 3: HTMX with encoded IDs")
    print("-" * 40)
    print("BEFORE:")
    print('''  <button hx-post="/sms/bill/{{ bill.id }}/comment/">Comment</button>''')
    print("\nAFTER:")
    print('''  {% load id_encoder %}''')
    print('''  <button hx-post="/sms/bill/{{ bill.id|encode_id }}/comment/">Comment</button>''')


def demo_security_comparison():
    """Demo security improvement"""
    print("\n" + "="*80)
    print("DEMO 5: Security Improvement")
    print("="*80)
    
    print("\n❌ BEFORE (Integer IDs - Easy to Guess):")
    print("-" * 80)
    for i in range(1, 6):
        print(f"  /sms/bill/{i}/detail/  ← Attacker can try {i}, {i+1}, {i+2}...")
    
    print("\n✅ AFTER (Encoded IDs - Cannot Guess):")
    print("-" * 80)
    for i in range(1, 6):
        encoded = encode_id(i)
        print(f"  /sms/bill/{encoded}/detail/  ← No pattern, cannot enumerate")
    
    print("\n📊 Benefits:")
    print("  ✅ Cannot guess next/previous ID")
    print("  ✅ Hide total number of records")
    print("  ✅ Harder to scrape data")
    print("  ✅ Better privacy for users")


def demo_real_world_scenario():
    """Demo real-world usage scenario"""
    print("\n" + "="*80)
    print("DEMO 6: Real-World Scenario - Bill Management")
    print("="*80)
    
    # Simulate database records
    bills = [
        {'id': 101, 'ten': 'Hóa đơn tháng 1', 'amount': 3000000},
        {'id': 102, 'ten': 'Hóa đơn tháng 2', 'amount': 3200000},
        {'id': 103, 'ten': 'Hóa đơn tháng 3', 'amount': 3100000},
    ]
    
    print("\nScenario: Landlord viewing bill list")
    print("-" * 80)
    
    print("\nHTML Table (with encoded IDs):")
    print("""
<table class="table">
    <thead>
        <tr>
            <th>Reference</th>
            <th>Bill Name</th>
            <th>Amount</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>""")
    
    for bill in bills:
        encoded = encode_id(bill['id'])
        print(f"""        <tr>
            <td>{encoded}</td>
            <td>{bill['ten']}</td>
            <td>{bill['amount']:,} VNĐ</td>
            <td>
                <a href="/sms/bill/{encoded}/detail/">View</a>
                <a href="/sms/bill/{encoded}/pdf/">PDF</a>
            </td>
        </tr>""")
    
    print("""    </tbody>
</table>""")
    
    print("\n📧 Email notification with encoded link:")
    print("-" * 80)
    bill = bills[0]
    encoded = encode_id(bill['id'])
    print(f"""
Subject: New bill available

Dear Renter,

You have a new bill: {bill['ten']}
Amount: {bill['amount']:,} VNĐ

View bill: http://yoursite.com/sms/bill/{encoded}/detail/

---
Note: The URL uses secure reference '{encoded}' instead of bill ID.
""")


def demo_migration_steps():
    """Show migration steps"""
    print("\n" + "="*80)
    print("DEMO 7: Migration Steps for Your Project")
    print("="*80)
    
    print("""
STEP 1: Update urls.py (Add secure URLs, keep old ones)
-------------------------------------------------------
from django.urls import register_converter
from sms.utils.hashid_converter import HashidConverter

register_converter(HashidConverter, 'hashid')

urlpatterns = [
    # NEW Secure URLs
    path('bill/<hashid:bill_id>/detail/', views.bill_detail_view, name='bill_detail_secure'),
    
    # OLD URLs (keep for now)
    path('bill/<int:bill_id>/detail/', views.bill_detail_view, name='bill_detail'),
]


STEP 2: Update Templates
-------------------------
{% load id_encoder %}

<!-- Change from: -->
<a href="{% url 'bill_detail' bill_id=bill.id %}">View</a>

<!-- To: -->
<a href="{% url 'bill_detail_secure' bill_id=bill.id %}">View</a>


STEP 3: Test
------------
✅ Open bill list page
✅ Click on bill link
✅ Check URL is /bill/jR7qKm3p/detail/ (not /bill/123/detail/)
✅ Try to change hash manually → Should get 404
✅ Check email links work


STEP 4: Gradually Update All URLs
----------------------------------
Priority order:
1. Bills & Payments (HIGH PRIORITY)
2. Issues & Notifications
3. Contracts
4. Houses & Locations
5. Others


STEP 5: Remove Old URLs (After Testing)
----------------------------------------
After confirming secure URLs work everywhere, remove old patterns:

urlpatterns = [
    path('bill/<hashid:bill_id>/detail/', views.bill_detail_view, name='bill_detail'),
    # REMOVED: path('bill/<int:bill_id>/detail/', ...)
]
""")


def main():
    """Run all demos"""
    print("\n" + "="*80)
    print(" URL ID ENCODING DEMONSTRATION")
    print("="*80)
    
    try:
        demo_basic_encoding()
        demo_url_examples()
        demo_multiple_ids()
        demo_template_usage()
        demo_security_comparison()
        demo_real_world_scenario()
        demo_migration_steps()
        
        print("\n" + "="*80)
        print(" ✅ ALL DEMOS COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\n📖 For full implementation guide, see: URL_OBFUSCATION_GUIDE.md")
        print("🚀 Ready to implement! Start with bills/payments URLs.\n")
        
    except Exception as e:
        print(f"\n❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
