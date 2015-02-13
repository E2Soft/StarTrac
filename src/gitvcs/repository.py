from time import mktime
import time

from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.datetime_safe import datetime

from gitvcs import repo
from tasks import models

def local_repo():
    return repo

def clear_commit_events():
    for commit in models.Commit.objects.all():
        commit.delete()

def update_commit_events(current_user):
    
    def process_commit(commit):
        
        users = User.objects.filter(username=commit.committer)
        if users:
            user = users[0]
        else:
            user=None
        
        date = timezone.make_aware(datetime.fromtimestamp(mktime(time.gmtime(commit.committed_date))), timezone.get_default_timezone())
        
        models.Commit(hex_sha=commit.hexsha, message=commit.message , date_created=date, event_user=current_user, event_kind='C', committer_name=commit.committer, committer_user=user).save()
        
    def should_stop(commit):
        return not len(models.Commit.objects.filter(hex_sha=commit.hexsha)) == 0 # ako postoji vec u bazi
    
    procesor = BranchesProcessor(process_commit=process_commit, should_stop=should_stop)
    procesor.traverse_branches(local_repo())
    
class BranchesProcessor():

    def __init__(self, process_branch=None, process_commit=None, should_stop=None):
        self.process_branch = process_branch if process_branch else lambda b: None
        self.process_commit = process_commit if process_commit else lambda c: None
        self.should_stop = should_stop if should_stop else lambda c: False

    def traverse_branches(self, repo):
        for head in repo.heads:
            self.process_branch(head)
            self.traverse_commit(head.commit)
    
    def traverse_commit(self, commit):
        if self.should_stop(commit):
            return
        self.process_commit(commit)
        for parent in commit.parents:
            self.traverse_commit(parent)