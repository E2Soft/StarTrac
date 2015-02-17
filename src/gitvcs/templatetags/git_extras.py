from django import template
from django.contrib.auth.models import User

from gitvcs import repository
from django.core.urlresolvers import reverse


register = template.Library()

@register.filter
def to_local_date(commit_date):
    return repository.to_local_date(commit_date)

@register.filter
def shorter(lst):
    # first 9
    return lst[:9]

@register.filter
def resolve_committer(committer):
    users = User.objects.filter(email=committer.email)
    
    if users:
        return '<a href="'+reverse('author', kwargs={'pk':users[0].pk})+'">'+committer.name+'<a/>'
    else:
        return committer.name
