'''
Created on Dec 29, 2014

@author: Milos
'''
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
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
    
class MilestoneDetail(DetailView):
    model = Milestone
    template_name = 'tasks/mdetail.html'
    context_object_name='milestone'
    
    def get_context_data(self, **kwargs):
        context = super(MilestoneDetail, self).get_context_data(**kwargs)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
     
        return context
    
class MilestoneUpdate(UpdateView):
    model = Milestone
    fields = ["date_created", "name", "summry"]
    template_name = 'tasks/mupdate.html'
    
    def get_success_url(self):
        return reverse('mdetail',args=(self.get_object().id,))
    
    def get_context_data(self, **kwargs):
        context = super(MilestoneDetail, self).get_context_data(**kwargs)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
     
        return context