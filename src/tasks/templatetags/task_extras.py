'''
Created on Jan 2, 2015

@author: Milos
'''
from django import template


register = template.Library()

@register.filter
def commnets(milestone):
    """Filtrira milestone tako da nadje samo broj komentara za svaki pojedinacni"""
    comments = milestone.event_set.filter(event_kind="K")
    size = comments.count()
    
    return size

@register.filter
def closedtasks(milestone):#Z state_kind .task_set.all.count
    """"""
    closed_tasks = milestone.task_set.filter(state_kind="Z")
    size = closed_tasks.count()
    
    return size

@register.filter
def percentage(milestone):
    """"""
    closed_tasks = milestone.task_set.filter(state_kind="Z")
    part = closed_tasks.count()
    
    all_tasks = milestone.task_set.all()
    whole = all_tasks.count()
    
    if(part != 0 and whole != 0):
        return round(100 * float(part)/float(whole),2)
    
    return 0