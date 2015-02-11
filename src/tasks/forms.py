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
        fields = ["name", "summry"]
    
    def __init__(self, *args, **kwargs):
        super(MilestoneForm, self).__init__(*args, **kwargs)
        self.fields["summry"].widget = widgets.AdminTextareaWidget()
        self.fields["summry"].widget.attrs['class']='form-control'
        self.fields["summry"].widget.attrs['rows']='5'
        
        self.fields["name"].widget.attrs['class']='form-control'
    
    def save(self, commit=True):
        instance = super(MilestoneForm, self).save(commit=False)
        
        if instance.date_created is None:
            instance.date_created = timezone.now()
        
        if commit:
            instance.save()
        return instance

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
    fields = ["date_created", "name", "summry"]
    template_name = 'tasks/mupdate.html'
    form_class = MilestoneForm
    
    def get_success_url(self):
        return reverse('mdetail',args=(self.get_object().id,))
    
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
    
class RequirementUpdate(UpdateView):
    model = Requirement
    fields = ["name", "state_kind", "project_tast_user", "priority_lvl", "pub_date", "content", "resolve_type"]
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
    form_class = RequirementForm
    
    def get_success_url(self):
        return reverse('requirements')

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

def determine_task_state(on_wait, assigned, resolved):
    if resolved:
        return 'Z' # Closed
    elif assigned:
        return 'P' # Accepted
    elif on_wait:
        return 'O' # On wait
    else:
        return 'C' # Created
    
class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'priority_lvl', 'requirement', 'milestone', 'assigned_to', 'is_on_wait', 'content']
    
    content = forms.CharField(widget=forms.Textarea)
    is_on_wait = forms.BooleanField(initial=False, required=False)
    
    def __init__(self, current_user, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        self.current_user = current_user
    
    def save(self, commit=True):
        instance = super(TaskCreateForm, self).save(commit=False)
        
        instance.pub_date = timezone.now()
        instance.project_tast_user = self.current_user
        instance.state_kind = determine_task_state(on_wait=self.cleaned_data.get('is_on_wait'),
                                                   assigned=self.cleaned_data.get('assigned_to'),
                                                   resolved=False)
        
        if commit:
            instance.save()
        return instance
    
class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'priority_lvl', 'requirement', 'milestone', 'assigned_to', 'resolve_type', 'is_on_wait', 'content']
    
    content = forms.CharField(widget=forms.Textarea)
    is_on_wait = forms.BooleanField(required=False)
    
    def __init__(self, current_user, *args, **kwargs):
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        self.fields["is_on_wait"].initial = (self.instance.state_kind == 'O')
        self.current_user = current_user
    
    def save(self, commit=True):
        instance = super(TaskUpdateForm, self).save(commit=False)
        
        old_state = get_object_or_404(Task,pk=instance.pk).state_kind
        
        instance.state_kind = determine_task_state(on_wait=self.cleaned_data.get('is_on_wait'),
                                                   assigned=self.cleaned_data.get('assigned_to'),
                                                   resolved=self.cleaned_data.get('resolve_type') != 'N') # 'N' = Open
        
        if commit:
            instance.save()
            if old_state != instance.state_kind:
                StateChange(new_state=instance.state_kind, event_user=self.current_user, event_kind='S', date_created=timezone.now(), requirement_task=instance).save()
        
        return instance


