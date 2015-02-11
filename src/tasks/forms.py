'''
Created on Dec 29, 2014

@author: Milos
'''
from itertools import groupby

from django import forms
from django.contrib.admin import widgets
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView

from tasks.models import Milestone, Requirement, StateChange, Event, Task


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ["name", "summary"]
    
    def __init__(self, *args, **kwargs):
        super(MilestoneForm, self).__init__(*args, **kwargs)
        self.fields["summary"].widget = widgets.AdminTextareaWidget()
        self.fields["summary"].widget.attrs['class']='form-control'
        self.fields["summary"].widget.attrs['rows']='5'
        
        self.fields["name"].widget.attrs['class']='form-control'

class MilestonesList(ListView):
    model = Milestone
    template_name = 'tasks/milestones.html'
    
    def get_queryset(self):
        return Milestone.objects.all()
    
class MilestoneDetail(DetailView):
    model = Milestone
    template_name = 'tasks/mdetail.html'
    context_object_name='milestone'
    
class MilestoneUpdate(UpdateView):
    model = Milestone
    fields = ["name", "summary"]
    template_name = 'tasks/mupdate.html'
    form_class = MilestoneForm
    
    def get_success_url(self):
        return reverse('mdetail',args=(self.get_object().id,))
    
class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ["name", "state_kind", "priority_lvl", "content", "resolve_type"]
    
    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        
        self.fields["content"].widget = widgets.AdminTextareaWidget()
        self.fields["content"].widget.attrs['rows']='5'
        
        for field in self.fields.values():
            field.widget.attrs['class']='form-control'

class RequirementCreateForm(RequirementForm):
    class Meta:
        model = Requirement
        fields = ["name", "state_kind", "priority_lvl", "content"]
            
class RequirementsList(ListView):
    model = Requirement
    template_name = 'tasks/requirements.html'
    
    def get_queryset(self):
        return Requirement.objects.all()
    
class RequirementDetail(DetailView):
    model = Requirement
    template_name = 'tasks/rdetail.html'
    context_object_name='requirement'
    
class RequirementUpdate(UpdateView):
    model = Requirement
    template_name = 'tasks/rupdate.html'
    form_class = RequirementForm
    
    def get_success_url(self):
        return reverse('rdetail',args=(self.get_object().id,))
    
    def form_valid(self, form):
        self.object = form.save(commit=False)

        #izmena stanja
        state_var = self.request.POST.get("state_kind",None)
        pk = self.get_object().id
        requirement = get_object_or_404(Requirement,pk=pk)
        
        if(state_var != requirement.state_kind):
            state_change = StateChange(event_user=self.request.user, event_kind="S",
                                       date_created=timezone.now(),requirement_task=requirement,
                                       milestone=None,new_state=state_var)
            state_change.save()

        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class RequiremenCreate(CreateView):
    model = Requirement
    template_name = 'tasks/addrequirement.html'
    form_class = RequirementCreateForm
    
    def get_success_url(self):
        return reverse('requirements')
    
    def form_valid(self, form):
        form.instance.pub_date = timezone.now()
        form.instance.project_tast_user = self.request.user
        
        return super(RequiremenCreate, self).form_valid(form)
    
def extract_date(entity):
    'extracts the starting date from an entity'
    return entity.date_created.date()

class TimelineList(ListView):
    model = Event
    template_name = 'tasks/timeline.html'
    
    def get_queryset(self):
        
        #results = Event.objects.values('date_created').annotate(dcount=Count('date_created'))
        
        entities = Event.objects.order_by('date_created')
        list_of_lists = [list(g) for _, g in groupby(entities, key=extract_date)]

        return list_of_lists
    
class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'priority_lvl', 'requirement', 'milestone', 'assigned_to', 'is_on_wait', 'content']
    
    content = forms.CharField(widget=forms.Textarea)
    is_on_wait = forms.BooleanField(initial=False, required=False)
    
    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class']='form-control'
        self.fields["is_on_wait"].widget.attrs['class']=''

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'priority_lvl', 'requirement', 'milestone', 'assigned_to', 'resolve_type', 'is_on_wait', 'content']
    
    content = forms.CharField(widget=forms.Textarea)
    is_on_wait = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        self.fields["is_on_wait"].initial = (self.instance.state_kind == 'O')
        for field in self.fields.values():
            field.widget.attrs['class']='form-control'
        self.fields["is_on_wait"].widget.attrs['class']=''

