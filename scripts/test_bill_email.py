"""
Script test gửi email hóa đơn PDF

Cách sử dụng:
    python test_bill_email.py <bill_id>

Ví dụ:
    python test_bill_email.py 123
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CollegeERP.settings')
django.setup()

from sms.models import Hoadon
from sms.views import send_bill_email_with_pdf


def test_send_bill_email(bill_id):
    """Test gửi email cho một hóa đơn cụ thể"""
    try:
        bill = Hoadon.objects.get(id=bill_id)
        print(f"\n=== THÔNG TIN HÓA ĐƠN ===")
        print(f"ID: {bill.id}")
        print(f"Tên: {bill.ten}")
        print(f"Nhà trọ: {bill.house.ten}")
        print(f"Kỳ: {bill.duedate.strftime('%m/%Y')}")
        print(f"Tổng tiền: {bill.TONG_CONG:,.0f} VNĐ")
        
        if not bill.renter:
            print("\n❌ ERROR: Hóa đơn không có người thuê!")
            return False
        
        print(f"\n=== THÔNG TIN NGƯỜI THUÊ ===")
        print(f"Họ tên: {bill.renter.hoten}")
        print(f"SĐT: {bill.renter.sdt}")
        print(f"Email: {bill.renter.email if bill.renter.email else 'KHÔNG CÓ'}")
        
        if not bill.renter.email:
            print("\n❌ ERROR: Người thuê không có địa chỉ email!")
            return False
        
        print(f"\n📧 Đang gửi email tới {bill.renter.email}...")
        result = send_bill_email_with_pdf(bill)
        
        if result:
            print("✅ GỬI EMAIL THÀNH CÔNG!")
            print(f"📨 Email đã được gửi tới: {bill.renter.email}")
            return True
        else:
            print("❌ GỬI EMAIL THẤT BẠI!")
            print("Vui lòng kiểm tra:")
            print("  1. Cấu hình EMAIL trong CollegeERP/info.py")
            print("  2. Internet connection")
            print("  3. Email account settings (Less secure app access)")
            return False
            
    except Hoadon.DoesNotExist:
        print(f"❌ ERROR: Không tìm thấy hóa đơn với ID: {bill_id}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_bill_email.py <bill_id>")
        print("\nDanh sách hóa đơn có sẵn:")
        
        from sms.models import Hoadon
        bills = Hoadon.objects.select_related('house', 'renter').all()[:10]
        
        if not bills:
            print("  Không có hóa đơn nào trong database")
        else:
            for bill in bills:
                email_status = "✓" if (bill.renter and bill.renter.email) else "✗"
                renter_name = bill.renter.hoten if bill.renter else "N/A"
                print(f"  ID {bill.id}: {bill.house.ten} - {renter_name} [{email_status} email]")
        
        sys.exit(1)
    
    bill_id = sys.argv[1]
    success = test_send_bill_email(bill_id)
    sys.exit(0 if success else 1)
