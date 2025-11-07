from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Location, House, Renter, HouseRenter, Hoadon, XaPhuong


class OwnerScopingTests(TestCase):
    def setUp(self):
        User = get_user_model()

        # Users
        self.superuser = User.objects.create_superuser(username="admin", email="a@a.com", password="pass")
        self.landlord1 = User.objects.create_user(username="ll1", email="l1@a.com", password="pass")
        self.landlord2 = User.objects.create_user(username="ll2", email="l2@a.com", password="pass")

        # Common XaPhuong
        self.xp = XaPhuong.objects.create(ma="001", ten="Phuong A", tp="TP X")

        # Locations
        self.loc1 = Location.objects.create(chu=self.landlord1, diachi="DC1", xp=self.xp)
        self.loc2 = Location.objects.create(chu=self.landlord2, diachi="DC2", xp=self.xp)

        # Houses
        self.house1 = House.objects.create(
            loc=self.loc1, ten="Nha 1", loainha="Nguyên căn", sophong=1,
            dientich=10, permonth=1000000, interval="1 tháng", deposit=1000000,
            kitchen=True, wc=True, aircondition=True, wifi=True, washingmachine=False
        )
        self.house2 = House.objects.create(
            loc=self.loc2, ten="Nha 2", loainha="Nguyên căn", sophong=1,
            dientich=10, permonth=1000000, interval="1 tháng", deposit=1000000,
            kitchen=True, wc=True, aircondition=True, wifi=True, washingmachine=False
        )

        # Renters
        self.renter1 = Renter.objects.create(chu_id=self.landlord1.id, hoten="R1")
        self.renter2 = Renter.objects.create(chu_id=self.landlord2.id, hoten="R2")

        # Contract tying renter1 to house1 (landlord1)
        HouseRenter.objects.create(house=self.house1, renter=self.renter1, active=True)

        # Bills
        self.bill1 = Hoadon.objects.create(house=self.house1, renter=self.renter1, ten="B1", duedate=timezone.now().date())
        self.bill2 = Hoadon.objects.create(house=self.house2, renter=self.renter2, ten="B2", duedate=timezone.now().date())

    def test_loc_list_scoped(self):
        self.client.force_login(self.landlord1)
        resp = self.client.get(reverse('loc_list'))
        self.assertEqual(resp.status_code, 200)
        # Template context key is 'loca' (paged)
        loca = resp.context.get('loca')
        self.assertIsNotNone(loca)
        ids = [obj.id for obj in loca]
        self.assertIn(self.loc1.id, ids)
        self.assertNotIn(self.loc2.id, ids)

    def test_house_list_requires_ownership(self):
        self.client.force_login(self.landlord1)
        # Access own location
        resp_ok = self.client.get(reverse('house_list', args=[self.loc1.id]))
        self.assertEqual(resp_ok.status_code, 200)
        # Access other landlord's location should 404 (guard via get_object_or_404)
        resp_forbidden = self.client.get(reverse('house_list', args=[self.loc2.id]))
        self.assertEqual(resp_forbidden.status_code, 404)

    def test_renter_list_scoped(self):
        self.client.force_login(self.landlord1)
        resp = self.client.get(reverse('renter_list'))
        self.assertEqual(resp.status_code, 200)
        renters = resp.context.get('renters')
        self.assertIsNotNone(renters)
        names = [r.hoten for r in renters]
        self.assertIn("R1", names)
        self.assertNotIn("R2", names)

    def test_bill_list_scoped(self):
        self.client.force_login(self.landlord1)
        resp = self.client.get(reverse('bill_list', args=[self.loc1.id]))
        self.assertEqual(resp.status_code, 200)
        bills = resp.context.get('bills')
        self.assertIsNotNone(bills)
        ids = [b.id for b in bills]
        self.assertIn(self.bill1.id, ids)
        self.assertNotIn(self.bill2.id, ids)

    def test_invoice_search_scoped(self):
        self.client.force_login(self.landlord1)
        resp = self.client.get(reverse('invoice_search'))
        self.assertEqual(resp.status_code, 200)
        page_obj = resp.context.get('page_obj')
        self.assertIsNotNone(page_obj)
        bill_ids = [b.id for b in page_obj]
        self.assertIn(self.bill1.id, bill_ids)
        self.assertNotIn(self.bill2.id, bill_ids)
