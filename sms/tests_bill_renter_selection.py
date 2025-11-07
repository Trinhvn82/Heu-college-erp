"""
Test Renter Selection in Bill Creation
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from sms.models import Location, House, Renter, HouseRenter, Hoadon, XaPhuong
from sms.forms import CreateHoaDonForm
from datetime import date, timedelta
from decimal import Decimal


class BillRenterSelectionTestCase(TestCase):
    """Test renter selection when creating bills"""
    
    def setUp(self):
        """Create test data"""
        # Create XaPhuong
        self.xp = XaPhuong.objects.create(
            ten="Phường Test",
            tenquan="Quận Test",
            tentinh="TP Test"
        )
        
        # Create landlord
        self.landlord = User.objects.create_user(
            username='landlord',
            password='test123'
        )
        
        # Create location
        self.loc = Location.objects.create(
            ten="Test Location",
            chu=self.landlord,
            xp=self.xp,
            diachi="123 Test St"
        )
        
        # Create house
        self.house = House.objects.create(
            ten="House 1",
            loc=self.loc,
            permonth=1000000,
            deposit=2000000,
            loainha="Phòng trọ"
        )
        
        # Create renters
        self.renter1 = Renter.objects.create(
            hoten="Renter Active",
            chu_id=self.landlord.id,
            sdt="0123456789"
        )
        self.renter2 = Renter.objects.create(
            hoten="Renter Previous",
            chu_id=self.landlord.id,
            sdt="0987654321"
        )
        self.renter3 = Renter.objects.create(
            hoten="Renter No Contract",
            chu_id=self.landlord.id,
            sdt="0111111111"
        )
        
        # Create contracts
        # Active contract with renter1
        self.contract1 = HouseRenter.objects.create(
            house=self.house,
            renter=self.renter1,
            rent_from=date.today() - timedelta(days=30),
            rent_to=date.today() + timedelta(days=335),
            active=True
        )
        
        # Previous (inactive) contract with renter2
        self.contract2 = HouseRenter.objects.create(
            house=self.house,
            renter=self.renter2,
            rent_from=date.today() - timedelta(days=365),
            rent_to=date.today() - timedelta(days=35),
            active=False
        )
        
        # renter3 has no contract with this house
        
        self.client = Client()
        self.client.login(username='landlord', password='test123')
    
    def test_form_shows_all_renters_with_contracts(self):
        """Form should show all renters who have/had contracts with the house"""
        form = CreateHoaDonForm(house=self.house)
        
        renter_queryset = form.fields['renter'].queryset
        renter_ids = list(renter_queryset.values_list('id', flat=True))
        
        # Should include renter1 (active) and renter2 (previous)
        self.assertIn(self.renter1.id, renter_ids)
        self.assertIn(self.renter2.id, renter_ids)
        
        # Should NOT include renter3 (no contract)
        self.assertNotIn(self.renter3.id, renter_ids)
    
    def test_form_defaults_to_active_renter(self):
        """Form should default to the renter with active contract"""
        form = CreateHoaDonForm(house=self.house)
        
        # Initial value should be renter1 (active contract)
        self.assertEqual(form.fields['renter'].initial, self.renter1)
    
    def test_can_create_bill_with_active_renter(self):
        """Should be able to create bill with active renter"""
        response = self.client.post(
            f'/create_bill/{self.house.id}/',
            {
                'renter': self.renter1.id,
                'ten': 'Test Bill',
                'duedate': (date.today() + timedelta(days=30)).isoformat(),
                'tienthuenha': '1000000',
                'tiendien': '200000',
                'tiennuoc': '100000',
                'tienkhac': '0',
            }
        )
        
        # Should succeed (redirect)
        self.assertEqual(response.status_code, 302)
        
        # Bill should be created with renter1
        bill = Hoadon.objects.filter(house=self.house).first()
        self.assertIsNotNone(bill)
        self.assertEqual(bill.renter, self.renter1)
    
    def test_can_create_bill_with_previous_renter(self):
        """Should be able to create bill with previous (inactive) renter"""
        response = self.client.post(
            f'/create_bill/{self.house.id}/',
            {
                'renter': self.renter2.id,  # Previous renter
                'ten': 'Test Bill Previous',
                'duedate': (date.today() + timedelta(days=30)).isoformat(),
                'tienthuenha': '1000000',
                'tiendien': '200000',
                'tiennuoc': '100000',
                'tienkhac': '0',
            }
        )
        
        # Should succeed
        self.assertEqual(response.status_code, 302)
        
        # Bill should be created with renter2
        bill = Hoadon.objects.filter(house=self.house, ten='Test Bill Previous').first()
        self.assertIsNotNone(bill)
        self.assertEqual(bill.renter, self.renter2)
    
    def test_cannot_create_bill_with_unrelated_renter(self):
        """Should NOT be able to create bill with renter who has no contract"""
        response = self.client.post(
            f'/create_bill/{self.house.id}/',
            {
                'renter': self.renter3.id,  # No contract with this house
                'ten': 'Test Bill Invalid',
                'duedate': (date.today() + timedelta(days=30)).isoformat(),
                'tienthuenha': '1000000',
                'tiendien': '200000',
                'tiennuoc': '100000',
                'tienkhac': '0',
            },
            follow=True
        )
        
        # Should fail (stay on same page with errors)
        self.assertEqual(response.status_code, 200)
        
        # Should have error message
        messages = list(response.context['messages'])
        self.assertTrue(any('không có hợp đồng' in str(m).lower() for m in messages))
        
        # Bill should NOT be created
        bill = Hoadon.objects.filter(house=self.house, ten='Test Bill Invalid').first()
        self.assertIsNone(bill)
    
    def test_can_create_bill_without_renter(self):
        """Should be able to create bill without specifying renter"""
        response = self.client.post(
            f'/create_bill/{self.house.id}/',
            {
                'renter': '',  # No renter selected
                'ten': 'Test Bill No Renter',
                'duedate': (date.today() + timedelta(days=30)).isoformat(),
                'tienthuenha': '1000000',
                'tiendien': '200000',
                'tiennuoc': '100000',
                'tienkhac': '0',
            }
        )
        
        # Should succeed
        self.assertEqual(response.status_code, 302)
        
        # Bill should be created without renter
        bill = Hoadon.objects.filter(house=self.house, ten='Test Bill No Renter').first()
        self.assertIsNotNone(bill)
        self.assertIsNone(bill.renter)
    
    def test_form_help_text_updates_based_on_contracts(self):
        """Form help text should indicate contract status"""
        # With contracts
        form_with_contracts = CreateHoaDonForm(house=self.house)
        self.assertIn("từng có hợp đồng", form_with_contracts.fields['renter'].help_text)
        
        # Create new house with no contracts
        house_no_contract = House.objects.create(
            ten="House No Contract",
            loc=self.loc,
            permonth=1500000,
            deposit=3000000,
            loainha="Phòng trọ"
        )
        
        form_no_contracts = CreateHoaDonForm(house=house_no_contract)
        self.assertIn("chưa có hợp đồng", form_no_contracts.fields['renter'].help_text)
