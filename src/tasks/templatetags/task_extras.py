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
def closedtasks(milestone):
    """Filtrira taskove, uzimajuci samo one koji su zatvoreni i vraca njihov broj"""
    closed_tasks = milestone.task_set.filter(state_kind="Z")
    size = closed_tasks.count()
    
    return size

@register.filter
def percentage(milestone):
    """Filter koji racuina procentualno koliko je posla uradjeno"""
    closed_tasks = milestone.task_set.filter(state_kind="Z")
    part = closed_tasks.count()
    
    all_tasks = milestone.task_set.all()
    whole = all_tasks.count()
    
    if(part != 0 and whole != 0):
        return round(100 * float(part)/float(whole),2)
    
    return 0

@register.filter
def showname(keyvalue):
    """filter koji za neku od prosledjenih kljuceva vraca vrednost"""
    key_dict ={'P':'Accepted','C': 'Created','Z': 'Closed','O': 'On Wait'}
    
    return key_dict[keyvalue]

@register.filter
def paintborder(priority):
    """filter koji dodaje boju za vaznost"""
    key_dict ={'C':'#ce2b37','H': '#ee6c3a','M': '#41783f','L': '#3d70b6'}
    
    return key_dict[priority]