'''
Created on Dec 29, 2014

@author: Milos
'''
from django import forms
from django.contrib.admin import widgets
from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from tasks.models import Milestone
from django.forms.widgets import Textarea


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ["date_created", "name", "summry"]
    
    def __init__(self, *args, **kwargs):
        super(MilestoneForm, self).__init__(*args, **kwargs)
        self.fields['date_created'].widget.attrs['class'] = 'form-control'
        self.fields["summry"].widget = widgets.AdminTextareaWidget()
        self.fields["summry"].widget.attrs['class']='form-control'
        self.fields["summry"].widget.attrs['rows']='5'
        
        self.fields["name"].widget.attrs['class']='form-control'
        self.fields["date_created"].widget.attrs['id']='datepicker'

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
    form_class = MilestoneForm
    
    def get_success_url(self):
        return reverse('mdetail',args=(self.get_object().id,))
    
    def get_context_data(self, **kwargs):
        context = super(MilestoneUpdate, self).get_context_data(**kwargs)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
     
        return context