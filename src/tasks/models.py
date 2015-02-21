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
        ('N', 'Open'),
        ('F', 'Fixed'),
        ('I', 'Invalid'),
        ('W', 'Wontfix'),
        ('D', 'Duplicate'),
        ('R', 'Worksforme'),
    )

class UserExtend(User):
    
    ''' 
    veza 1-1 da bi mogli lakse da pristupimo slici: 
    # npr. user.UserExtend.picture 
    '''
    user = models.OneToOneField(User)
    
    '''
    slika moze biti null, u tom slucaju korisniku dodeljujemo
    neku podrazumevanu sliku
    '''
    picture = models.ImageField(upload_to='album', blank = True, null = True)
    
    '''
    user toString()
    '''
    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=20, default="")
    color = models.CharField(max_length=8, default="#000000")
    
    def __str__(self):
        return self.name

class RequirementTask(models.Model):
    name = models.CharField(max_length=70, default="")
    state_kind = models.CharField(max_length=1, choices=STATE_KIND, default="C")
    project_tast_user = models.ForeignKey(User)
    priority_lvl = models.CharField(max_length=1, choices=PRIORITY_LVL, default="L")
    pub_date = models.DateTimeField('date published')
    content = models.CharField(max_length=100, default="")
    resolve_type = models.CharField(max_length=1, choices=RESOLVE_TYPE, default="N")
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    
    class Meta:
        abstract = False
        ordering = ['name']
     
    def __str__(self):
        return self.name
    
    def getstate(self):
        for t in STATE_KIND:
            if(t[0]==self.state_kind):
                return t[1]
    
    def getpriority(self):
        for t in PRIORITY_LVL:
            if(t[0]==self.priority_lvl):
                return t[1]
    
    def getresolve(self):
        for t in RESOLVE_TYPE:
            if(t[0]==self.resolve_type):
                return t[1]

class Requirement(RequirementTask):
    pass
  
class Milestone(models.Model):
    date_created = models.DateTimeField('date published')
    name = models.CharField(max_length=70, default="")
    summary =  models.CharField(max_length=300)
    
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
    
    def iscomment(self):
        return self.event_kind == "K"
    
    def geteventkind(self):
        for t in EVENT_KIND:
            if(t[0]==self.event_kind):
                return t[1]

class Task(RequirementTask):
    requirement = models.ForeignKey(Requirement, null=True, blank=True)
    milestone = models.ForeignKey(Milestone, null=True, blank=True)
    assigned_to = models.ForeignKey(User, null=True, blank=True)

class Comment(Event):
    content = models.CharField(max_length=200, default="")
    
class StateChange(Event):
    new_state = models.CharField(max_length=1, choices=STATE_KIND, default="C")
    
    def getstate(self):
        for t in STATE_KIND:
            if(t[0]==self.new_state):
                return t[1]
    
class Commit(Event):
    hex_sha = models.CharField(max_length=40)
    message = models.CharField(max_length=300)
    committer_name = models.CharField(max_length=70, null=True, blank=True)
    committer_user = models.ForeignKey(User, null=True)
    
