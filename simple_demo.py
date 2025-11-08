"""
Simple demo of Hashids encoding/decoding without Django
Shows how IDs are transformed for URLs

Run: python simple_demo.py
"""

from hashids import Hashids

# Configuration (matching settings.py)
SALT = '3n821tz@-e98qd96+h_=+hgo1uv1*0d2@dfko#_ft@11pmu-secret-salt'
MIN_LENGTH = 8
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

# Initialize Hashids
hashids = Hashids(salt=SALT, min_length=MIN_LENGTH, alphabet=ALPHABET)


def demo_basic():
    """Basic encoding demo"""
    print("\n" + "="*80)
    print("DEMO 1: Basic ID Encoding")
    print("="*80)
    
    test_ids = [1, 10, 123, 456, 1000, 9999, 12345]
    
    print("\n{:>10} → {:<20}".format("Integer ID", "Encoded Hash"))
    print("-" * 40)
    
    for id_num in test_ids:
        encoded = hashids.encode(id_num)
        decoded = hashids.decode(encoded)[0]
        match = "✓" if decoded == id_num else "✗"
        print(f"  {id_num:>8} → {encoded:<18} {match}")


def demo_urls():
    """URL transformation demo"""
    print("\n" + "="*80)
    print("DEMO 2: URL Security Comparison")
    print("="*80)
    
    print("\n❌ BEFORE (Exposed Integer IDs):")
    print("-" * 80)
    for i in [1, 2, 3, 4, 5]:
        print(f"  /sms/bill/{i}/detail/")
    print("\n  Problem: Attacker can easily guess and try IDs 1, 2, 3, 4, 5...")
    
    print("\n✅ AFTER (Encoded Hashed IDs):")
    print("-" * 80)
    for i in [1, 2, 3, 4, 5]:
        encoded = hashids.encode(i)
        print(f"  /sms/bill/{encoded}/detail/")
    print("\n  Benefit: No pattern visible, cannot enumerate!")


def demo_real_world():
    """Real-world examples"""
    print("\n" + "="*80)
    print("DEMO 3: Real-World URL Examples")
    print("="*80)
    
    examples = [
        ("Bill Detail", 123, "/sms/bill/{}/detail/"),
        ("Bill PDF", 456, "/sms/bill/{}/pdf/"),
        ("Payment", 789, "/sms/payment/confirm/{}/"),
        ("Issue", 42, "/sms/issues/{}/"),
        ("House", 15, "/sms/house/{}/bills/"),
    ]
    
    print("\n{:20} {:12} → {:<30}".format("Feature", "ID", "Secure URL"))
    print("-" * 80)
    
    for name, id_num, pattern in examples:
        encoded = hashids.encode(id_num)
        url = pattern.format(encoded)
        print(f"  {name:18} {id_num:>10} → {url}")


def demo_roundtrip():
    """Test encode/decode roundtrip"""
    print("\n" + "="*80)
    print("DEMO 4: Encode/Decode Roundtrip Test")
    print("="*80)
    
    print("\n{:>10} → {:^20} → {:>10} {:^10}".format(
        "Original", "Encoded", "Decoded", "Match?"))
    print("-" * 60)
    
    test_ids = [1, 50, 100, 999, 5000, 99999]
    
    for original in test_ids:
        encoded = hashids.encode(original)
        decoded = hashids.decode(encoded)[0]
        match = "✅ PASS" if decoded == original else "❌ FAIL"
        print(f"  {original:>8} → {encoded:^18} → {decoded:>8} {match}")


def demo_security_benefits():
    """Show security improvements"""
    print("\n" + "="*80)
    print("DEMO 5: Security Benefits")
    print("="*80)
    
    print("""
📊 Attack Scenario Comparison:

WITHOUT Encoding (Integer IDs):
--------------------------------
Attacker sees: /bill/123/detail/
Attacker tries:
  - /bill/122/detail/ (previous bill)
  - /bill/124/detail/ (next bill)
  - /bill/1/detail/ to /bill/10000/detail/ (scan all)
  
❌ Result: Can access all bills, enumerate users, scrape data

WITH Encoding (Hashed IDs):
----------------------------
Attacker sees: /bill/jR7qKm3p/detail/
Attacker tries:
  - /bill/jR7qKm3q/detail/ (random guess)
  - /bill/AAAAAAAA/detail/ (brute force)
  - Cannot determine pattern or next ID
  
✅ Result: Cannot enumerate, cannot guess, must know exact hash

Security Improvements:
----------------------
✅ Prevents enumeration attacks
✅ Hides database size (can't tell if you have 10 or 10,000 records)
✅ Makes automated scraping much harder
✅ Protects user privacy
✅ Adds obscurity layer (not encryption, but helps)
""")


def demo_template_examples():
    """Show template usage"""
    print("\n" + "="*80)
    print("DEMO 6: Django Template Usage")
    print("="*80)
    
    print("""
Example 1: Simple Link
-----------------------
BEFORE:
    <a href="{% url 'bill_detail' bill_id=123 %}">View Bill</a>
    
AFTER:
    {% load id_encoder %}
    <a href="{% url 'bill_detail' bill_id=123|encode_id %}">View Bill</a>
    
Generated HTML:
    <a href="/sms/bill/jR7qKm3p/detail/">View Bill</a>


Example 2: Display Reference Number
------------------------------------
BEFORE:
    <p>Bill Reference: #{{ bill.id }}</p>
    <!-- Shows: Bill Reference: #123 -->
    
AFTER:
    {% load id_encoder %}
    <p>Bill Reference: #{{ bill.id|encode_id }}</p>
    <!-- Shows: Bill Reference: #jR7qKm3p -->


Example 3: HTMX Button
-----------------------
BEFORE:
    <button hx-post="/sms/bill/{{ bill.id }}/comment/">
        Add Comment
    </button>
    
AFTER:
    {% load id_encoder %}
    <button hx-post="/sms/bill/{{ bill.id|encode_id }}/comment/">
        Add Comment
    </button>
""")


def demo_implementation_steps():
    """Show implementation steps"""
    print("\n" + "="*80)
    print("DEMO 7: Implementation Steps for Your Project")
    print("="*80)
    
    print("""
STEP 1: Already Installed ✅
-----------------------------
- hashids library installed
- id_encoder.py created
- hashid_converter.py created
- Template tags created
- Settings configured


STEP 2: Test Encoding (You Are Here)
-------------------------------------
- Run this demo: python simple_demo.py
- Verify encoding/decoding works
- Review security benefits


STEP 3: Update URLs (Choose Approach)
--------------------------------------
Approach A: Using Template Filters (Easy, No URL Changes)
    - Update templates only
    - Keep existing urls.py
    - Example: {{ bill.id|encode_id }}
    
Approach B: Using URL Converter (Better, Requires URL Changes)
    - Update urls.py with hashid converter
    - Update templates
    - Example: path('bill/<hashid:bill_id>/', ...)


STEP 4: Priority URLs to Secure
--------------------------------
HIGH PRIORITY:
1. Bills & Payments
2. Issues & Notifications  
3. Contracts

MEDIUM PRIORITY:
4. Houses
5. Locations
6. Renters

LOW PRIORITY:
7. Admin URLs
8. Internal features


STEP 5: Test & Deploy
----------------------
- Test all links work
- Check emails/notifications
- Verify no broken URLs
- Deploy to production
- Monitor for issues


Next Action:
------------
📖 Read: URL_OBFUSCATION_GUIDE.md for detailed instructions
🚀 Start: Update bill-related templates first
""")


def main():
    """Run all demos"""
    print("\n" + "="*80)
    print(" 🔐 URL ID ENCODING DEMONSTRATION")
    print(" Securing URLs by Encoding Integer IDs")
    print("="*80)
    
    try:
        demo_basic()
        demo_urls()
        demo_real_world()
        demo_roundtrip()
        demo_security_benefits()
        demo_template_examples()
        demo_implementation_steps()
        
        print("\n" + "="*80)
        print(" ✅ DEMO COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\n📚 Documentation:")
        print("   - Full Guide: URL_OBFUSCATION_GUIDE.md")
        print("   - Utils: sms/utils/id_encoder.py")
        print("   - Templates: sms/templatetags/id_encoder.py")
        print("\n🎯 Next Steps:")
        print("   1. Review URL_OBFUSCATION_GUIDE.md")
        print("   2. Start with bill URLs (highest priority)")
        print("   3. Test thoroughly before production")
        print("")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
