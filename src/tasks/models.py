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

class ProjectTask(models.Model):
    name = models.CharField(max_length=70, default="")
    state_kind = models.CharField(max_length=1, choices=STATE_KIND, default="C")
    project_tast_user = models.ForeignKey(User, null=True)
    priority_lvl = models.CharField(max_length=1, choices=PRIORITY_LVL, default="L")
    
    class Meta:
        abstract = True
        ordering = ['name']
     
    def __str__(self):
        return self.name

class Project(ProjectTask):
    pub_date = models.DateTimeField('date published')

class Task(ProjectTask):
    projects = models.ForeignKey(Project)
    
class Milestone(ProjectTask):
    summry =  models.CharField(max_length=300)