from django.contrib.auth.models import User
from django.db import models


#Enumeracija koja ce biti koriscena dalje u projektu
STATE_KIND = (
        ('P', 'Accepted'),
        ('C', 'Created'),
        ('Z', 'Closed'),
        ('O', 'On Wait'),
    )

EVENT_KIND = (
        ('C', 'Accepted'),
        ('P', 'Created'),
    )

PRIORITY_LVL= (
        ('C', 'Critical'),
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    )

class RequirementTask(models.Model):
    name = models.CharField(max_length=70, default="")
    state_kind = models.CharField(max_length=1, choices=STATE_KIND, default="C")
    project_tast_user = models.ForeignKey(User)
    priority_lvl = models.CharField(max_length=1, choices=PRIORITY_LVL, default="L")
    
    class Meta:
        abstract = False
        ordering = ['name']
     
    def __str__(self):
        return self.name

class Requirement(RequirementTask):
    pub_date = models.DateTimeField('date published')
    
class Event(models.Model):
    event_user = models.ForeignKey(User)
    event_kind = models.CharField(max_length=1, choices=EVENT_KIND, default="C")
    date_created = models.DateTimeField('date published')
    requirement_task = models.ForeignKey(RequirementTask)
    
    class Meta:
        abstract = False

class Milestone(models.Model):
    date_created = models.DateTimeField('date published')
    name = models.CharField(max_length=70, default="")
    summry =  models.CharField(max_length=300)
    event = models.ForeignKey(Event, null=True)

class Task(RequirementTask):
    projects = models.ForeignKey(Requirement, null=True)
    milestone = models.ForeignKey(Milestone, null=True)

class Comment(Event):
    content = models.CharField(max_length=200, default="")
    
class StateChange(Event):
    new_state = models.CharField(max_length=1, choices=STATE_KIND, default="C")