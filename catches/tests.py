from django.test import TestCase, Client
from django.contrib.auth.models import User
from catches.models import Lake, Fish, Stock, Fly, Log
import json
import datetime

class MobileLogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testangler', password='password123')
        self.lake = Lake.objects.create(name='Test Lake', lat=53.5, long=-113.5)
        self.fish = Fish.objects.create(name='Rainbow Trout', abbreviation='RNTR')
        self.stock = Stock.objects.create(
            lake=self.lake, 
            fish=self.fish, 
            number=1000, 
            length=18.0, 
            date_stocked=datetime.date.today()
        )
        self.fly = Fly.objects.create(name='Chironomid')
        self.client = Client()

    def test_mobile_log_requires_login(self):
        response = self.client.get('/mobile-log/')
        self.assertEqual(response.status_code, 302)

    def test_mobile_log_desktop_blocked(self):
        self.client.force_login(self.user)
        response = self.client.get('/mobile-log/', HTTP_USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mobile-Only Catch Logger')

    def test_mobile_log_mobile_access(self):
        self.client.force_login(self.user)
        response = self.client.get('/mobile-log/', HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Quick Catch')
        self.assertContains(response, 'Rainbow Trout')

    def test_mobile_log_preview_mode(self):
        self.client.force_login(self.user)
        response = self.client.get('/mobile-log/?preview=1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Quick Catch')

    def test_lake_stocked_fish_api(self):
        self.client.force_login(self.user)
        response = self.client.get(f'/api/lake-stocked-fish/{self.lake.id}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['lake_id'], self.lake.id)
        self.assertEqual(len(data['fish']), 1)
        self.assertEqual(data['fish'][0]['name'], 'Rainbow Trout')

    def test_mobile_log_submit_api(self):
        self.client.force_login(self.user)
        payload = {
            'lake_id': self.lake.id,
            'fish_id': self.fish.id,
            'fly_id': self.fly.id,
            'fly_size': '#14',
            'fly_colour': 'Black',
            'length': '16.0',
            'length_unit': 'in',
            'weight': '2.0',
            'weight_unit': 'lbs',
            'gps_lat': 53.5461,
            'gps_long': -113.4938
        }
        response = self.client.post(
            '/api/mobile-log-submit/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['fish_name'], 'Rainbow Trout')
        self.assertEqual(data['length_in'], 16.0)

        # Verify DB entry
        created_log = Log.objects.get(id=data['log_id'])
        self.assertEqual(created_log.angler, self.user)
        self.assertEqual(created_log.lake, self.lake)
        self.assertEqual(created_log.fish, self.fish)
        self.assertEqual(created_log.fly, self.fly)
        self.assertEqual(created_log.len_inch, 16.0)
