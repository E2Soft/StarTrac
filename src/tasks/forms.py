'''
Created on Dec 29, 2014

@author: Milos
'''
from django.views.generic.list import ListView

from tasks.models import Milestone


class MilestonesList(ListView):
    model = Milestone
    template_name = 'tasks/milestones.html'
    
    def get_queryset(self):
        return Milestone.objects.all()
    
    """def get_context_data(self, **kwargs):
        context = super(MilestonesList, self).get_context_data(**kwargs)
        
        context["back"] = self.request.META["HTTP_REFERER"]      
        return context"""