'''
Created on Dec 29, 2014

@author: Milos
'''
from django import forms
from django.contrib.admin import widgets
from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory
from django.forms.widgets import Textarea
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView

from tasks.models import Milestone, Requirement


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
    
class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ["name", "state_kind", "project_tast_user", "priority_lvl", "pub_date", "content", "resolve_type"]
    
    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        self.fields['pub_date'].widget.attrs['class'] = 'form-control'
        self.fields["pub_date"].widget.attrs['id']='datepicker'
        
        self.fields["content"].widget = widgets.AdminTextareaWidget()
        self.fields["content"].widget.attrs['class']='form-control'
        self.fields["content"].widget.attrs['rows']='5'
        
        self.fields["name"].widget.attrs['class']='form-control'
        self.fields["state_kind"].widget.attrs['class']='form-control'
        self.fields["project_tast_user"].widget.attrs['class']='form-control'
        self.fields["priority_lvl"].widget.attrs['class']='form-control'
        self.fields["resolve_type"].widget.attrs['class']='form-control'
            
class RequirementsList(ListView):
    model = Requirement
    template_name = 'tasks/requirements.html'
    
    def get_queryset(self):
        return Requirement.objects.all()
    
class RequirementDetail(DetailView):
    model = Requirement
    template_name = 'tasks/rdetail.html'
    context_object_name='requirement'
    
    def get_context_data(self, **kwargs):
        context = super(RequirementDetail, self).get_context_data(**kwargs)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
     
        return context
    
class RequirementUpdate(UpdateView):
    model = Requirement
    fields = ["name", "state_kind", "project_tast_user", "priority_lvl", "pub_date", "content", "resolve_type"]
    template_name = 'tasks/rupdate.html'
    form_class = RequirementForm
    
    def get_success_url(self):
        return reverse('rdetail',args=(self.get_object().id,))
    
    def get_context_data(self, **kwargs):
        context = super(RequirementUpdate, self).get_context_data(**kwargs)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
     
        return context

class RequiremenCreate(CreateView):
    model = Requirement
    template_name = 'tasks/addrequirement.html'
    form_class = RequirementForm
    
    def get_success_url(self):
        return reverse('requirements')
    
    def get_context_data(self, **kwargs):
        context = super(RequiremenCreate, self).get_context_data(**kwargs)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
     
        return context