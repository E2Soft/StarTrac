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
        ('K', 'Comment'),
        ('C', 'Commit'),
        ('S', 'StateChange'),
    )

PRIORITY_LVL= (
        ('C', 'Critical'),
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    )

RESOLVE_TYPE = (
        ('N', 'None'),
        ('F', 'Fixed'),
        ('I', 'Invalid'),
        ('W', 'Wontfix'),
        ('D', 'Duplicate'),
        ('R', 'Worksforme'),
    )

class RequirementTask(models.Model):
    name = models.CharField(max_length=70, default="")
    state_kind = models.CharField(max_length=1, choices=STATE_KIND, default="K")
    project_tast_user = models.ForeignKey(User)
    priority_lvl = models.CharField(max_length=1, choices=PRIORITY_LVL, default="L")
    pub_date = models.DateTimeField('date published')
    content = models.CharField(max_length=100, default="")
    resolve_type = models.CharField(max_length=1, choices=RESOLVE_TYPE, default="F")
    
    class Meta:
        abstract = False
        ordering = ['name']
     
    def __str__(self):
        return self.name

class Requirement(RequirementTask):
    pass
  
class Milestone(models.Model):
    date_created = models.DateTimeField('date published')
    name = models.CharField(max_length=70, default="")
    summry =  models.CharField(max_length=300)
    
    def __str__(self):
        return self.name 
    
class Event(models.Model):
    event_user = models.ForeignKey(User)
    event_kind = models.CharField(max_length=1, choices=EVENT_KIND, default="C")
    date_created = models.DateTimeField('date published')
    requirement_task = models.ForeignKey(RequirementTask, blank=True, null=True)
    milestone = models.ForeignKey(Milestone, null=True, blank=True)
    
    class Meta:
        abstract = False

class Task(RequirementTask):
    projects = models.ForeignKey(Requirement, null=True, blank=True)
    milestone = models.ForeignKey(Milestone, null=True, blank=True)
    assigned_to = models.ForeignKey(User, null=True, blank=True)

class Comment(Event):
    content = models.CharField(max_length=200, default="")
    
class StateChange(Event):
    new_state = models.CharField(max_length=1, choices=STATE_KIND, default="C")
    
class Commit(Event):
    commit_url = models.URLField()