from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone

from tasks.forms import MilestoneDetail, TimelineList
from tasks.models import Milestone


# Create your tests here.
"""
    pokretanje:
        python manage.py test 
        ili desni klik na projekat > Django > run Django Django Tests
"""

class SimpleTestCase(TestCase):
    def setUp(self):
        milestone = Milestone.objects.create(date_created=timezone.now(),name="Test",summary="Test adding new Milestone")
    
    def test_timeline_view(self):
        resp = self.client.get('/timeline/')
        self.assertEqual(resp.status_code, 200)
    
    def test_fake_url(self):
        resp = self.client.get('/jovan/')
        self.assertEqual(resp.status_code, 404)
        
    def test_fake_url_reverse(self):
        resp = self.client.get('/jovan/')
        self.assertNotEqual(resp.status_code, 200)
        
    def test_milestones_number(self):
        milestone = Milestone.objects.get(pk=1)
        
        self.assertEqual(milestone.name, "Test")
        self.assertEqual(Milestone.objects.all().count(), 1)
        
    def test_milestones_name(self):
        milestone = Milestone.objects.get(pk=1)
        
        self.assertEqual(milestone.name, "Test")
        
    def test_client(self):
        c = Client()
        resp =  c.get(reverse('mdetail', args=(2,)))
        self.assertEqual(resp.status_code, 404)
        