from django.db import models

# Create your models here.
class Project(models.Model):
    project_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.project_name

class Task(models.Model):
    projects = models.ForeignKey(Project)
    task_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.task_name