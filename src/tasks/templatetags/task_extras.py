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

@register.tag
def task_priority_style(parser, token):
    '''
    Vraca bs-callout bootstrap stil sa bojom u zavisnosti od prioriteta i stanja taska.
    '''
    try:
        _, task = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return CurrentTimeNode(task)

class CurrentTimeNode(template.Node):
    def __init__(self, task):
        self.task_unresolved = template.Variable(task)
    
    def render(self, context):
        
        task = self.task_unresolved.resolve(context)
        
        if task.state_kind == 'Z':
            return ""
        
        style_prefix = "bs-callout-"
        
        if task.priority_lvl == 'L':
            style = "success"
        elif task.priority_lvl == 'M':
            style = "info"
        elif task.priority_lvl == 'H':
            style = "warning"
        elif task.priority_lvl == 'C':
            style = "danger"
        
        return style_prefix+style
        