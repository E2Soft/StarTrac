# Create your tests here.
# Create your tests here.
"""
    pokretanje:
        python manage.py test 
        ili desni klik na projekat > Django > run Django Django Tests
"""

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
from django.utils import timezone

from tasks import views
from tasks.models import Milestone, Task


class SimpleTestCase(TestCase):
    def setUp(self):
        Milestone.objects.create(date_created=timezone.now(),name="Test",summary="Test adding new Milestone")
        self.user = User.objects.create_user(username='jacob', email='jacob@asd.com', password='top_secret')
        self.client.login(username='jacob', password='top_secret')
    
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
        
class TasksTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jacob', email='jacob@asd.com', password='top_secret')
        self.client.login(username='jacob', password='top_secret')
        self.created_task = Task.objects.create(pub_date=timezone.now(), name="TestTask", content="Test adding new Task", project_tast_user=self.user)
        self.onwait_task = Task.objects.create(pub_date=timezone.now(), name="onwait_task", content="Test adding new Task", project_tast_user=self.user, state_kind='O')
        self.accepted_task = Task.objects.create(pub_date=timezone.now(), name="accepted_task", content="Test adding new Task", project_tast_user=self.user, assigned_to=self.user, state_kind='P')
        self.closed_task = Task.objects.create(pub_date=timezone.now(), name="closed_tasks", content="Test adding new Task", project_tast_user=self.user, assigned_to=self.user, state_kind='Z')
        
    def test_name(self):
        task = Task.objects.get(pk=self.created_task.pk)
        self.assertEqual(task.name, self.created_task.name)
    
    def test_state_kind(self):
        self.assertEqual(Task.objects.get(pk=self.created_task.pk).state_kind, "C")
        self.assertEqual(Task.objects.get(pk=self.onwait_task.pk).state_kind, "O")
        self.assertEqual(Task.objects.get(pk=self.accepted_task.pk).state_kind, "P")
        self.assertEqual(Task.objects.get(pk=self.closed_task.pk).state_kind, "Z")
        
    def test_project_tast_user(self):
        task = Task.objects.get(pk=self.created_task.pk)
        self.assertEqual(task.project_tast_user.username, self.user.username)
        
    def test_assigned_to_user(self):
        task = Task.objects.get(pk=self.accepted_task.pk)
        self.assertEqual(task.assigned_to.username, self.user.username)

    def test_default_priority_lvl(self):
        task = Task.objects.get(pk=self.created_task.pk)
        self.assertEqual(task.priority_lvl, "L")
    
    def test_default_resolve_type(self):
        task = Task.objects.get(pk=self.created_task.pk)
        self.assertEqual(task.resolve_type, "N")
        
    def test_determine_task_state(self):
        self.assertEqual(views.determine_task_state(on_wait=False, assigned=False, resolved=False), "C")
        self.assertEqual(views.determine_task_state(on_wait=True, assigned=False, resolved=False), "O")
        self.assertEqual(views.determine_task_state(on_wait=False, assigned=True, resolved=False), "P")
        self.assertEqual(views.determine_task_state(on_wait=True, assigned=True, resolved=False), "P")
        self.assertEqual(views.determine_task_state(on_wait=False, assigned=True, resolved=True), "Z")
        self.assertEqual(views.determine_task_state(on_wait=False, assigned=False, resolved=True), "Z")
        
    def test_task_list(self):
        resp = self.client.get(reverse('tasks'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['task_list'])
        task_list = resp.context['task_list']
        self.assertEqual(len(task_list), 4)
        self.assertTrue(self.created_task in task_list)
        self.assertTrue(self.onwait_task in task_list)
        self.assertTrue(self.accepted_task in task_list)
        self.assertTrue(self.closed_task in task_list)
    
    def test_task_detail(self):
        resp = self.client.get(reverse('tdetail', args=[self.created_task.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['task'])
        task = resp.context['task']
        self.assertEqual(task.name, self.created_task.name)
    
    def test_StatisticsIndexView_task_count(self):
        sv = views.StatisticsIndexView()
        self.assertEqual(sv.created_tasks(), 1)
        self.assertEqual(sv.onwait_tasks(), 1)
        self.assertEqual(sv.accepted_tasks(), 1)
        self.assertEqual(sv.closed_tasks(), 1)

    