'''
Created on Dec 29, 2014

@author: Milos
'''
from itertools import groupby

from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView

from gitvcs.repository import update_commit_events
from tasks.models import Milestone, Requirement, StateChange, PriorityChange, \
    ResolveEvent, AddEvent, Event, Task, Tag


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
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MilestonesList, self).dispatch(*args, **kwargs)
    
    def get_queryset(self):
        return Milestone.objects.all()
    
class MilestoneDetail(DetailView):
    model = Milestone
    template_name = 'tasks/mdetail.html'
    context_object_name='milestone'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MilestoneDetail, self).dispatch(*args, **kwargs)
    
class MilestoneUpdate(UpdateView):
    model = Milestone
    fields = ["name", "summary"]
    template_name = 'tasks/mupdate.html'
    form_class = MilestoneForm
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MilestoneUpdate, self).dispatch(*args, **kwargs)
    
    def get_success_url(self):
        return reverse('mdetail',args=(self.get_object().id,))
    
class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ["name", "state_kind", "priority_lvl", "content", "resolve_type","tags"]
    
    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        self.fields["content"].widget = widgets.AdminTextareaWidget()
        self.fields["content"].widget.attrs['class']='form-control'
        self.fields["content"].widget.attrs['rows']='5'
        
        self.fields["name"].widget.attrs['class']='form-control'
        self.fields["state_kind"].widget.attrs['class']='form-control'
        self.fields["priority_lvl"].widget.attrs['class']='form-control'
        self.fields["resolve_type"].widget.attrs['class']='form-control'
        self.fields["tags"].widget.attrs['class']='form-control'
            
class RequirementsList(ListView):
    model = Requirement
    template_name = 'tasks/requirements.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RequirementsList, self).dispatch(*args, **kwargs)
    
    def get_queryset(self):
        return Requirement.objects.all()
    
class RequirementDetail(DetailView):
    model = Requirement
    template_name = 'tasks/rdetail.html'
    context_object_name='requirement'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RequirementDetail, self).dispatch(*args, **kwargs)
    
class RequirementUpdate(UpdateView):
    model = Requirement
    template_name = 'tasks/rupdate.html'
    form_class = RequirementForm
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RequirementUpdate, self).dispatch(*args, **kwargs)
    
    def get_success_url(self):
        return reverse('rdetail',args=(self.get_object().id,))
    
    def form_valid(self, form):
        self.object = form.save(commit=False)

        #izmena stanja
        state_var = self.request.POST.get("state_kind",None)
        
        response = super(RequirementUpdate, self).form_valid(form)
        
        pk = self.get_object().id
        requirement = get_object_or_404(Requirement,pk=pk)
        
        if(state_var != requirement.state_kind):
            state_change = StateChange(event_user=self.request.user, event_kind="S",
                                       date_created=timezone.now(),requirement_task=requirement,
                                       milestone=None,new_state=state_var)
            state_change.save()
        
        #izmena prioriteta
        priority_var = self.request.POST.get("priority_lvl",None)
        if(priority_var != requirement.priority_lvl):
            priority_change = PriorityChange(event_user=self.request.user, event_kind="P",
                                       date_created=timezone.now(),requirement_task=requirement,
                                       milestone=None,new_priority=priority_var)
            priority_change.save()
        
        #izmena resolve-a
        resolve_var = self.request.POST.get("priority_lvl",None)
        
        if(resolve_var != requirement.resolve_type):
            resolve_change = ResolveEvent(event_user=self.request.user, event_kind="R",
                                       date_created=timezone.now(),requirement_task=requirement,
                                       milestone=None,new_resolve=resolve_var)
            resolve_change.save()
            
        self.object.save()
        
        return response

class RequiremenCreate(CreateView):
    model = Requirement
    template_name = 'tasks/addrequirement.html'
    form_class = RequirementForm
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RequiremenCreate, self).dispatch(*args, **kwargs)
    
    def get_success_url(self):
        return reverse('requirements')
    
    def form_valid(self, form):
        form.instance.pub_date = timezone.now()
        form.instance.project_tast_user = self.request.user
        
        response = super(RequiremenCreate, self).form_valid(form)
    
        #add event
        add_req = AddEvent(event_user=self.request.user, event_kind="A",date_created=timezone.now(),
                           requirement_task=form.instance,milestone=None)
        add_req.save()
    
        return response
    
def extract_date(entity):
    'extracts the starting date from an entity'
    return entity.date_created.date()

class TimelineList(ListView):
    model = Event
    template_name = 'tasks/timeline.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TimelineList, self).dispatch(*args, **kwargs)
    
    def get_queryset(self):
        
        update_commit_events(self.request.user)
        
        entities = Event.objects.order_by('date_created').reverse()
        list_of_lists = [list(g) for _, g in groupby(entities, key=extract_date)]

        return list_of_lists
    
class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'priority_lvl', 'requirement', 'milestone', 'assigned_to', 'is_on_wait', 'content',"tags"]
    
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
        fields = ['name', 'priority_lvl', 'requirement', 'milestone', 'assigned_to', 'resolve_type', 'is_on_wait', 'content',"tags"]
    
    content = forms.CharField(widget=forms.Textarea)
    is_on_wait = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        self.fields["is_on_wait"].initial = (self.instance.state_kind == 'O')
        for field in self.fields.values():
            field.widget.attrs['class']='form-control'
        self.fields["is_on_wait"].widget.attrs['class']=''

class TagsList(ListView):
    model = Tag
    template_name = 'tasks/tags.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TagsList, self).dispatch(*args, **kwargs)
    
    def get_queryset(self):
        return Tag.objects.all()
    
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name", "color"]
    
    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs['class']='form-control'
        self.fields["color"].widget.attrs['class']='form-control'
        self.fields["color"].widget.attrs['id']='colorpickerfield'
        
class TagCreate(CreateView):
    model = Tag
    template_name = 'tasks/addtag.html'
    form_class = TagForm
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TagCreate, self).dispatch(*args, **kwargs)
    
    def get_success_url(self):
        return reverse('tags')
    
    def get_context_data(self, **kwargs):
        context = super(TagCreate, self).get_context_data(**kwargs)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
     
        return context


class TagDetail(DetailView):
    model = Tag
    template_name = 'tasks/tagdetail.html'
    context_object_name='tag'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TagDetail, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(TagDetail, self).get_context_data(**kwargs)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
     
        return context
    

class TagUpdate(UpdateView):
    model = Tag
    template_name = 'tasks/tagupdate.html'
    form_class = TagForm
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TagUpdate, self).dispatch(*args, **kwargs)
    
    def get_success_url(self):
        return reverse('tagdetail',args=(self.get_object().id,))
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        
        response = super(TagUpdate, self).form_valid(form)
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super(TagUpdate, self).get_context_data(**kwargs)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
     
        return context
