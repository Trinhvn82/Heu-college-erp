"""
Test parameter validation for ownership checks
Ensures users can only access resources they own
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from sms.models import Location, House, Renter, HouseRenter, Hoadon, Thanhtoan, XaPhuong
from decimal import Decimal
from datetime import date, timedelta


class ParameterValidationTestCase(TestCase):
    """Test that ID parameters are validated for ownership"""
    
    def setUp(self):
        """Create test users and data"""
        # Create XaPhuong for Location
        self.xp = XaPhuong.objects.create(
            ten="Phường Test",
            tenquan="Quận Test",
            tentinh="TP Test"
        )
        
        # Create users
        self.landlord1 = User.objects.create_user(
            username='landlord1',
            password='testpass123'
        )
        self.landlord2 = User.objects.create_user(
            username='landlord2',
            password='testpass123'
        )
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@test.com'
        )
        
        # Create locations for each landlord
        self.loc1 = Location.objects.create(
            ten="Location 1",
            chu=self.landlord1,
            xp=self.xp,
            diachi="123 Test St"
        )
        self.loc2 = Location.objects.create(
            ten="Location 2",
            chu=self.landlord2,
            xp=self.xp,
            diachi="456 Test St"
        )
        
        # Create houses
        self.house1 = House.objects.create(
            ten="House 1-1",
            loc=self.loc1,
            permonth=1000000,
            deposit=2000000,
            loainha="Phòng trọ"
        )
        self.house2 = House.objects.create(
            ten="House 2-1",
            loc=self.loc2,
            permonth=1500000,
            deposit=3000000,
            loainha="Chung cư mini"
        )
        
        # Create renters
        self.renter1 = Renter.objects.create(
            hoten="Renter 1",
            chu_id=self.landlord1.id,
            sdt="0123456789"
        )
        self.renter2 = Renter.objects.create(
            hoten="Renter 2",
            chu_id=self.landlord2.id,
            sdt="0987654321"
        )
        
        # Create contracts
        self.contract1 = HouseRenter.objects.create(
            house=self.house1,
            renter=self.renter1,
            rent_from=date.today(),
            rent_to=date.today() + timedelta(days=365),
            active=True
        )
        self.contract2 = HouseRenter.objects.create(
            house=self.house2,
            renter=self.renter2,
            rent_from=date.today(),
            rent_to=date.today() + timedelta(days=365),
            active=True
        )
        
        # Create bills
        self.bill1 = Hoadon.objects.create(
            house=self.house1,
            ngay_tao=date.today(),
            duedate=date.today() + timedelta(days=30),
            TIEN_NHA=Decimal('1000000'),
            TONG_CONG=Decimal('1000000'),
            SO_TIEN_DA_TRA=Decimal('0'),
            CONG_NO=Decimal('1000000'),
            status='ChuaTT'
        )
        self.bill2 = Hoadon.objects.create(
            house=self.house2,
            ngay_tao=date.today(),
            duedate=date.today() + timedelta(days=30),
            TIEN_NHA=Decimal('1500000'),
            TONG_CONG=Decimal('1500000'),
            SO_TIEN_DA_TRA=Decimal('0'),
            CONG_NO=Decimal('1500000'),
            status='ChuaTT'
        )
        
        # Create payment
        self.payment1 = Thanhtoan.objects.create(
            hoadon=self.bill1,
            tientt=Decimal('500000'),
            ngaytt=date.today(),
            status='Choxn'
        )
        
        self.client = Client()
    
    def test_location_access_validation(self):
        """Test that landlords can only access their own locations"""
        # Login as landlord1
        self.client.login(username='landlord1', password='testpass123')
        
        # Can access own location
        response = self.client.get(f'/view_loc/{self.loc1.id}/')
        self.assertEqual(response.status_code, 200)
        
        # Cannot access other landlord's location (redirects with error message)
        response = self.client.get(f'/view_loc/{self.loc2.id}/', follow=True)
        self.assertEqual(response.status_code, 200)  # Redirected to loc_list
        # Check for error message in context
        messages_list = list(response.context['messages'])
        self.assertTrue(any('không có quyền' in str(m) for m in messages_list))
    
    def test_location_edit_validation(self):
        """Test that landlords can only edit their own locations"""
        self.client.login(username='landlord1', password='testpass123')
        
        # Can access own location edit page
        response = self.client.get(f'/edit_loc/{self.loc1.id}/')
        self.assertEqual(response.status_code, 200)
        
        # Cannot access other landlord's location edit (redirects with error)
        response = self.client.get(f'/edit_loc/{self.loc2.id}/', follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertTrue(any('không có quyền' in str(m) for m in messages_list))
    
    def test_house_edit_validation(self):
        """Test that landlords can only edit houses in their locations"""
        self.client.login(username='landlord1', password='testpass123')
        
        # Can access own house edit
        response = self.client.get(f'/edit_house/{self.loc1.id}/{self.house1.id}/')
        self.assertEqual(response.status_code, 200)
        
        # Cannot access other landlord's house (redirects with error)
        response = self.client.get(f'/edit_house/{self.loc2.id}/{self.house2.id}/', follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertTrue(any('không có quyền' in str(m) for m in messages_list))
    
    def test_renter_edit_validation(self):
        """Test that landlords can only edit their own renters"""
        self.client.login(username='landlord1', password='testpass123')
        
        # Can access own renter
        response = self.client.get(f'/edit_renter/{self.renter1.id}/')
        self.assertEqual(response.status_code, 200)
        
        # Cannot access other landlord's renter (redirects with error)
        response = self.client.get(f'/edit_renter/{self.renter2.id}/', follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertTrue(any('không có quyền' in str(m) for m in messages_list))
    
    def test_contract_list_validation(self):
        """Test that landlords can only see contracts for their houses"""
        self.client.login(username='landlord1', password='testpass123')
        
        # Can access contracts for own house
        response = self.client.get(f'/hr_list/{self.house1.id}/')
        self.assertEqual(response.status_code, 200)
        
        # Cannot access contracts for other landlord's house (redirects with error)
        response = self.client.get(f'/hr_list/{self.house2.id}/', follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertTrue(any('không có quyền' in str(m) for m in messages_list))
    
    def test_bill_detail_validation(self):
        """Test that landlords can only view their own bills"""
        self.client.login(username='landlord1', password='testpass123')
        
        # Can view own bill
        response = self.client.get(f'/bill_detail/{self.bill1.id}/')
        self.assertEqual(response.status_code, 200)
        
        # Cannot view other landlord's bill (redirects with error)
        response = self.client.get(f'/bill_detail/{self.bill2.id}/', follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertTrue(any('không có quyền' in str(m) for m in messages_list))
    
    def test_payment_operations_validation(self):
        """Test that only bill owner can confirm/delete payments"""
        # Landlord2 tries to confirm payment for landlord1's bill
        self.client.login(username='landlord2', password='testpass123')
        
        response = self.client.get(f'/confirm_payment/{self.payment1.id}/', follow=True)
        self.assertEqual(response.status_code, 200)  # Redirected with error
        
        # Check for error message
        messages_list = list(response.context['messages'])
        self.assertTrue(any('không có quyền' in str(m) for m in messages_list))
        
        # Verify payment was not confirmed
        self.payment1.refresh_from_db()
        self.assertEqual(self.payment1.status, 'Choxn')
        
        # Login as correct landlord
        self.client.login(username='landlord1', password='testpass123')
        response = self.client.get(f'/confirm_payment/{self.payment1.id}/')
        self.assertEqual(response.status_code, 302)  # Should redirect after success
        
        # Verify payment was confirmed
        self.payment1.refresh_from_db()
        self.assertEqual(self.payment1.status, 'Daxn')
    
    def test_superuser_access_all(self):
        """Test that superuser can access all resources"""
        self.client.login(username='admin', password='adminpass123')
        
        # Can access all locations
        response = self.client.get(f'/view_loc/{self.loc1.id}/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(f'/view_loc/{self.loc2.id}/')
        self.assertEqual(response.status_code, 200)
        
        # Can access all bills
        response = self.client.get(f'/bill_detail/{self.bill1.id}/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(f'/bill_detail/{self.bill2.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_upload_file_validation(self):
        """Test that landlords can only upload files to their locations"""
        self.client.login(username='landlord1', password='testpass123')
        
        # Can access own location's upload page
        response = self.client.get(f'/upload_file_loc/{self.loc1.id}/')
        self.assertEqual(response.status_code, 200)
        
        # Cannot access other landlord's location upload (redirects with error)
        response = self.client.get(f'/upload_file_loc/{self.loc2.id}/', follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertTrue(any('không có quyền' in str(m) for m in messages_list))
    
    def test_invalid_id_returns_error(self):
        """Test that invalid IDs show error messages and redirect"""
        self.client.login(username='landlord1', password='testpass123')
        
        # Non-existent location - redirects to loc_list with error
        response = self.client.get('/view_loc/99999/', follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertTrue(any('Không tìm thấy' in str(m) for m in messages_list))
        
        # Non-existent house - redirects with error
        response = self.client.get('/edit_house/1/99999/', follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertTrue(len(messages_list) > 0)
        
        # Non-existent bill - redirects with error
        response = self.client.get('/bill_detail/99999/', follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertTrue(any('Không tìm thấy' in str(m) for m in messages_list))
