'''
Created on Jan 2, 2015

@author: Milos
'''
from django import template
from django.core.urlresolvers import reverse
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


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

@register.filter
def event_glyphicon_style(event):
    return {'K':"glyphicon-comment",
            'C':"glyphicon-record",
            'S':"glyphicon-cog",
                    }[event.event_kind]

@register.filter
def task_priority_style(task):
    
    if task.state_kind == 'Z':
        return ""
    
    style_prefix = "bs-callout-"
    
    return style_prefix + {'L':"success",
                           'M':"info",
                           'H':"warning",
                           'C':"danger",
                                        }[task.priority_lvl]

@register.filter
def event_summary(event):
    if event.requirement_task:
        if hasattr(event.requirement_task, 'task'):
            summary="Task "
        elif hasattr(event.requirement_task, 'requirement'):
            summary="Requirement "
        else:
            summary=''
        summary += '"'+event.requirement_task.name+'": '
    elif event.milestone:
        summary = '"Milestone "'+event.milestone.name+'": '
    else:
        summary = ''
    
    if event.event_kind == 'K':
        summary += event.comment.content
    elif event.event_kind == 'C':
        summary += event.commit.message
    elif event.event_kind == 'S':
        summary += event.statechange.getstate()
    
    max_length = 100
    
    if len(summary) > max_length:
        summary = summary[:max_length-3]+"..."
    else:
        summary = summary[:max_length]
    
    return summary

def do_escape(to_escape, autoescape):
    return conditional_escape(to_escape) if autoescape else to_escape

@register.filter
def event_user(event, autoescape=None):
    if event.event_kind == 'C':
        if event.commit.committer_user:
            user = event.commit.committer_user
            ret = """<a href="{author_url}"><span class="glyphicon glyphicon-user"></span> {user_name}</a>""".format(author_url=reverse('author', kwargs={'pk':user.pk}), user_name=do_escape(user.username, autoescape))
        else:
            ret = """<span class="glyphicon glyphicon-user"></span> {user_name}""".format(user_name=do_escape(event.commit.committer_name, autoescape))
    else:
        ret = """<a href="{author_url}"><span class="glyphicon glyphicon-user"></span> {user_name}</a>""".format(author_url=reverse('author', kwargs={'pk':event.event_user.pk}), user_name=do_escape(event.event_user.username, autoescape))
    
    return mark_safe(ret)



