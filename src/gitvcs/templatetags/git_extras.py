from django import template
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from gitvcs import repository


register = template.Library()

@register.filter
def to_local_date(commit_date):
    return repository.to_local_date(commit_date)

@register.filter
def shorter(lst):
    # first 9
    return lst[:9]

@register.filter
def resolve_committer(committer, autoescape=None):
    users = User.objects.filter(email=committer.email)
    
    if users:
        committer_name = conditional_escape(committer.name) if autoescape else committer.name
        return mark_safe('<a href="{link}">{title}</a>'.format(link=reverse('author', kwargs={'pk':users[0].pk}), title=committer_name))
    else:
        return committer.name