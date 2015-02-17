import json
from time import mktime
import time

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime
from git.objects.commit import Commit

from gitvcs import repo
from tasks import models

def local_repo():
    return repo

def clear_commit_events():
    for commit in models.Commit.objects.all():
        commit.delete()

def to_local_date(commit_date):
    return timezone.make_aware(datetime.fromtimestamp(mktime(time.gmtime(commit_date))), timezone.get_default_timezone())

def update_commit_events(current_user):
    
    for commit in commits():
        
        if not len(models.Commit.objects.filter(hex_sha=commit.hexsha)) == 0:
            break
        
        users = User.objects.filter(email=commit.committer.email)
        if users:
            user = users[0]
        else:
            user=None
        
        models.Commit(hex_sha=commit.hexsha, message=commit.message , date_created=to_local_date(commit.committed_date), event_user=current_user, event_kind='C', committer_name=commit.committer.name, committer_user=user).save()

def tree_as_json(tree, branch_name):
    
    root_dir = {'children':[]}
    
    def process_dir(parent_directory, tree):
        new_dir = {'id':tree.hexsha, 'name':tree.name, 'type':'dir', 'children':[]}
        parent_directory['children'].append(new_dir)
        return new_dir
    
    def process_file(parent_directory, file):
        parent_directory['children'].append({'id':file.hexsha, 'name':file.name, 'type':'file', 'url':reverse('file_contents')+"?branch="+branch_name+"&path="+file.path})
    
    processor = TreeProcessor(process_dir=process_dir, process_file=process_file)
    processor.traverse_tree(root_dir, tree)
    
    if root_dir['children']:
        return json.dumps(root_dir['children'][0]['children']) # get contents of a branch (branch is root dirs only child) and dump to json
    else:
        return []

def branches():
    return local_repo().branches

def _all_commits_generator():
    current_commits = [head.commit for head in local_repo().heads] # take all head commits
    
    while current_commits: # while there are commits
        current_commits.sort(key=lambda commit: commit.committed_date) # sort by date
        commit = current_commits.pop() # take the newest
        for parent in commit.parents: # add all parents
            if parent not in current_commits: # that are not already added
                current_commits.append(parent)
        yield commit

def commits(rev=None):
    if rev:
        return Commit.iter_items(local_repo(), rev)
    else:
        return _all_commits_generator()

class TreeProcessor():
    
    def __init__(self, process_dir=None, process_file=None):
        self.process_dir = process_dir if process_dir else lambda b: None
        self.process_file = process_file if process_file else lambda b: None
    
    def traverse_tree(self, parent_dir, tree):
        processed_dir = self.process_dir(parent_dir, tree)
        for sub_tree in tree.trees:
            self.traverse_tree(processed_dir, sub_tree)
        for blob in tree.blobs:
            self.process_file(processed_dir, blob)
    