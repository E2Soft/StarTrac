import json
import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.edit import UpdateView, CreateView
from collections import OrderedDict
from tasks.forms import MilestoneForm, TaskUpdateForm, TaskCreateForm
from tasks.models import Task, Milestone, Comment, Requirement, StateChange, \
    Event, AddEvent, PriorityChange, ResolveEvent
from django.views.generic.base import TemplateView

    # Create your views here.
def index(request):
    if request.user.is_authenticated():
        tasks = Task.objects.order_by('state_kind')
        ret_dict_order = OrderedDict()
        ret_dict_order["C"] = []
        ret_dict_order["O"] = []
        ret_dict_order["P"] = []
        ret_dict_order["Z"] = []
        
        for task in tasks:
            ret_dict_order[task.state_kind].append(task)
        
        context = {"isadmin":request.user.is_superuser,"username":request.user.username, "tasks":ret_dict_order}
        
        return render(request,'tasks/logged.html',context)
    else:
        return render(request,'tasks/index.html')

    
def mcomment(request):
    if request.POST:
        content = request.POST.get("content","")
        milestone_id = request.POST.get("pk","")
        date = timezone.now()
        milestone = get_object_or_404(Milestone,pk=milestone_id)

        comment = Comment(event_user=request.user,content=content,
                                  date_created=date,
                                  milestone=milestone,event_kind="K")
        comment.save()                                                         
    
    response_data = {}
    response_data['content'] = content
    response_data['date'] = date.__str__()
    response_data['user'] = request.user.username
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def addmilestone(request):
    if request.POST:
        form = MilestoneForm(request.POST)
        if form.is_valid():
            form.instance.date_created = timezone.now()
            form.save()
            
            #add event
            add_req = AddEvent(event_user=request.user, event_kind="A",date_created=timezone.now(),
                               requirement_task=None,milestone=form.instance)
            add_req.save()
            
            return HttpResponseRedirect(reverse('milestones'))
    else:
        form = MilestoneForm()
    
    back = ""
    try:
        back = request.META["HTTP_REFERER"]
    except(KeyError):
        back="/"
        
    return render(request,'tasks/addmilestone.html',{"form":form,
                                                     "back":back})
    
def rcomment(request):
    if request.POST:
        content = request.POST.get("content","")
        requirement_id = request.POST.get("pk","")
        date = timezone.now()
        requirement = get_object_or_404(Requirement,pk=requirement_id)

        comment = Comment(event_user=request.user,content=content,
                                  date_created=date,
                                  requirement_task=requirement,event_kind="K")
        comment.save()                                                         
    
    response_data = {}
    response_data['content'] = content
    response_data['date'] = date.__str__()
    response_data['user'] = request.user.username
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def testgraphpriority(request):
    request_pk = request.GET["pk"]   
    #print("REQ PK:{}".format(request_pk))
    milestone = get_object_or_404(Milestone,pk=request_pk)
    
    critical_tasks = milestone.task_set.filter(priority_lvl="C").count()
    high_tasks = milestone.task_set.filter(priority_lvl="H").count()
    medium_tasks = milestone.task_set.filter(priority_lvl="M").count()
    low_tasks = milestone.task_set.filter(priority_lvl="L").count()
    
    resp_list = []
    
    resp_obj = {}
    resp_obj['value'] = critical_tasks
    resp_obj['color'] = "#F7464A"
    resp_obj['highlight'] = "#FF5A5E"
    resp_obj['label'] = "Critical"
    
    resp_list.append(resp_obj)
    
    resp_obj1 = {}
    resp_obj1['value'] = high_tasks
    resp_obj1['color'] = "#46BFBD"
    resp_obj1['highlight'] = "#5AD3D1"
    resp_obj1['label'] = "High"
    
    resp_list.append(resp_obj1)
    
    resp_obj2 = {}
    resp_obj2['value'] = medium_tasks
    resp_obj2['color'] = "#FDB45C"
    resp_obj2['highlight'] = "#FFC870"
    resp_obj2['label'] = "Medium"
    
    resp_list.append(resp_obj2)
    
    resp_obj3 = {}
    resp_obj3['value'] = low_tasks
    resp_obj3['color'] = "#949FB1"
    resp_obj3['highlight'] = "#A8B3C5"
    resp_obj3['label'] = "Low"
    
    resp_list.append(resp_obj3)
    
    return HttpResponse(json.dumps(resp_list), content_type="application/json")

class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def kanban(request):
    rid = request.GET["id"]
    box = request.GET["box"]
    
    task = get_object_or_404(Task,pk=rid)
    ret_dict={}
    
    #if current state is not accepted it can't be closed!
    """if task.state_kind != "P" and box == "Z":
        return HttpResponseServerError("Closed can only be accepted task!")"""
    
    #print("ID:{} BOX:{}".format(rid, box))
    
    #proveri task i kako ga sacuvati
    task.state_kind = box
    
    if(task.state_kind == "P"):
        task.assigned_to = request.user
    
    #promena stanja    
    state_change = StateChange(event_user=request.user, event_kind="S",
                                           date_created=timezone.now(),requirement_task=task,
                                           milestone=task.milestone,new_state=box)
    state_change.save()
    
    #colors that represents priority
    key_dict ={'C':'#ce2b37','H': '#ee6c3a','M': '#41783f','L': '#3d70b6'}
    
    #states that can be in cloed task
    closed_dict={'F': 'Fixed','I': 'Invalid','W': 'Wontfix','D': 'Duplicate','R': 'Worksforme'}
    
    ret_dict["status"] = "Ok"
    ret_dict["data"] = {}
    ret_dict["code"] = "200"
    ret_dict["message"] = key_dict[task.priority_lvl]
    ret_dict["explaination"]= request.user.username
    ret_dict["created"]= "false"
    
    if task.state_kind ==  "Z":
        ret_dict["created"]= "true"
        ret_dict["closedlist"]=closed_dict
        task.resolve_type = "R"
        
    #update current task    
    task.save()
    
    return HttpResponse(json.dumps(ret_dict), content_type="application/json")


def testgraph(request):
    request_pk = request.GET["pk"]
    #print("REQ PK:{}".format(request_pk))   
    milestone = get_object_or_404(Milestone,pk=request_pk)
    
    closed_tasks = milestone.task_set.filter(state_kind="Z").count()
    onwait_tasks = milestone.task_set.filter(state_kind="O").count()
    accepted_tasks = milestone.task_set.filter(state_kind="P").count()
    created_tasks = milestone.task_set.filter(state_kind="C").count()
    
    resp_list = []
    
    resp_obj = {}
    resp_obj['value'] = closed_tasks
    resp_obj['color'] = "#F7464A"
    resp_obj['highlight'] = "#FF5A5E"
    resp_obj['label'] = "Closed"
    
    resp_list.append(resp_obj)
    
    resp_obj1 = {}
    resp_obj1['value'] = onwait_tasks
    resp_obj1['color'] = "#46BFBD"
    resp_obj1['highlight'] = "#5AD3D1"
    resp_obj1['label'] = "On wait"
    
    resp_list.append(resp_obj1)
    
    resp_obj2 = {}
    resp_obj2['value'] = accepted_tasks
    resp_obj2['color'] = "#FDB45C"
    resp_obj2['highlight'] = "#FFC870"
    resp_obj2['label'] = "Accepted"
    
    resp_list.append(resp_obj2)
    
    resp_obj3 = {}
    resp_obj3['value'] = created_tasks
    resp_obj3['color'] = "#949FB1"
    resp_obj3['highlight'] = "#A8B3C5"
    resp_obj3['label'] = "Created"
    
    resp_list.append(resp_obj3)
    
    return HttpResponse(json.dumps(resp_list), content_type="application/json")
    
    
def resolvegraph(request):
    request_pk = request.GET["pk"]
    #print("REQ PK:{}".format(request_pk))   
    milestone = get_object_or_404(Milestone,pk=request_pk)
    
    none_tasks = milestone.task_set.filter(resolve_type="N").count()
    fixed_tasks = milestone.task_set.filter(resolve_type="F").count()
    invalid_tasks = milestone.task_set.filter(resolve_type="I").count()
    wontfix_tasks = milestone.task_set.filter(resolve_type="W").count()
    duplicate_tasks = milestone.task_set.filter(resolve_type="D").count()
    worksforme_tasks = milestone.task_set.filter(resolve_type="R").count()
    
    resp_list = []

    resp_obj = {}
    resp_obj['value'] = none_tasks
    resp_obj['color'] = "#F7464A"
    resp_obj['highlight'] = "#FF5A5E"
    resp_obj['label'] = "None"
    
    resp_list.append(resp_obj)
    
    resp_obj1 = {}
    resp_obj1['value'] = fixed_tasks
    resp_obj1['color'] = "#46BFBD"
    resp_obj1['highlight'] = "#5AD3D1"
    resp_obj1['label'] = "Fixed"
    
    resp_list.append(resp_obj1)
    
    resp_obj2 = {}
    resp_obj2['value'] = invalid_tasks
    resp_obj2['color'] = "#FDB45C"
    resp_obj2['highlight'] = "#FFC870"
    resp_obj2['label'] = "Invalid"
    
    resp_list.append(resp_obj2)
    
    resp_obj3 = {}
    resp_obj3['value'] = wontfix_tasks
    resp_obj3['color'] = "#949FB1"
    resp_obj3['highlight'] = "#A8B3C5"
    resp_obj3['label'] = "Won't fix"
    
    resp_list.append(resp_obj3)
    
    resp_obj4 = {}
    resp_obj4['value'] = duplicate_tasks
    resp_obj4['color'] = "#4D5360"
    resp_obj4['highlight'] = "#616774"
    resp_obj4['label'] = "Duplicate"
    
    resp_list.append(resp_obj4)
    
    resp_obj5 = {}
    resp_obj5['value'] = worksforme_tasks
    resp_obj5['color'] = "#4D5360"
    resp_obj5['highlight'] = "#616774"
    resp_obj5['label'] = "Works for me"
    
    resp_list.append(resp_obj5)
    
    return HttpResponse(json.dumps(resp_list), content_type="application/json")
    
    
def reqgraph(request):
    request_pk = request.GET["pk"]
    #print("REQ PK:{}".format(request_pk))
    requirement = get_object_or_404(Requirement,pk=request_pk)
    
    closed_tasks = requirement.task_set.filter(state_kind="Z").count()
    onwait_tasks = requirement.task_set.filter(state_kind="O").count()
    accepted_tasks = requirement.task_set.filter(state_kind="P").count()
    created_tasks = requirement.task_set.filter(state_kind="C").count()
    
    resp_list = []
    
    resp_obj = {}
    resp_obj['value'] = closed_tasks
    resp_obj['color'] = "#F7464A"
    resp_obj['highlight'] = "#FF5A5E"
    resp_obj['label'] = "Closed"
    
    resp_list.append(resp_obj)
    
    resp_obj1 = {}
    resp_obj1['value'] = onwait_tasks
    resp_obj1['color'] = "#46BFBD"
    resp_obj1['highlight'] = "#5AD3D1"
    resp_obj1['label'] = "On wait"
    
    resp_list.append(resp_obj1)
    
    resp_obj2 = {}
    resp_obj2['value'] = accepted_tasks
    resp_obj2['color'] = "#FDB45C"
    resp_obj2['highlight'] = "#FFC870"
    resp_obj2['label'] = "Accepted"
    
    resp_list.append(resp_obj2)
    
    resp_obj3 = {}
    resp_obj3['value'] = created_tasks
    resp_obj3['color'] = "#949FB1"
    resp_obj3['highlight'] = "#A8B3C5"
    resp_obj3['label'] = "Created"
    
    resp_list.append(resp_obj3)
    
    return HttpResponse(json.dumps(resp_list), content_type="application/json")


def reqtestgraphpriority(request):
    request_pk = request.GET["pk"]   
    #print("REQ PK:{}".format(request_pk))
    requirement = get_object_or_404(Requirement,pk=request_pk)
    
    critical_tasks = requirement.task_set.filter(priority_lvl="C").count()
    high_tasks = requirement.task_set.filter(priority_lvl="H").count()
    medium_tasks = requirement.task_set.filter(priority_lvl="M").count()
    low_tasks = requirement.task_set.filter(priority_lvl="L").count()
    
    resp_list = []
    
    resp_obj = {}
    resp_obj['value'] = critical_tasks
    resp_obj['color'] = "#F7464A"
    resp_obj['highlight'] = "#FF5A5E"
    resp_obj['label'] = "Critical"
    
    resp_list.append(resp_obj)
    
    resp_obj1 = {}
    resp_obj1['value'] = high_tasks
    resp_obj1['color'] = "#46BFBD"
    resp_obj1['highlight'] = "#5AD3D1"
    resp_obj1['label'] = "High"
    
    resp_list.append(resp_obj1)
    
    resp_obj2 = {}
    resp_obj2['value'] = medium_tasks
    resp_obj2['color'] = "#FDB45C"
    resp_obj2['highlight'] = "#FFC870"
    resp_obj2['label'] = "Medium"
    
    resp_list.append(resp_obj2)
    
    resp_obj3 = {}
    resp_obj3['value'] = low_tasks
    resp_obj3['color'] = "#949FB1"
    resp_obj3['highlight'] = "#A8B3C5"
    resp_obj3['label'] = "Low"
    
    resp_list.append(resp_obj3)
    
    return HttpResponse(json.dumps(resp_list), content_type="application/json")


def reqresolvegraph(request):
    request_pk = request.GET["pk"]
    #print("REQ PK:{}".format(request_pk))   
    requirement = get_object_or_404(Requirement,pk=request_pk)
    
    none_tasks = requirement.task_set.filter(resolve_type="N").count()
    fixed_tasks = requirement.task_set.filter(resolve_type="F").count()
    invalid_tasks = requirement.task_set.filter(resolve_type="I").count()
    wontfix_tasks = requirement.task_set.filter(resolve_type="W").count()
    duplicate_tasks = requirement.task_set.filter(resolve_type="D").count()
    worksforme_tasks = requirement.task_set.filter(resolve_type="R").count()
    
    resp_list = []

    resp_obj = {}
    resp_obj['value'] = none_tasks
    resp_obj['color'] = "#F7464A"
    resp_obj['highlight'] = "#FF5A5E"
    resp_obj['label'] = "None"
    
    resp_list.append(resp_obj)
    
    resp_obj1 = {}
    resp_obj1['value'] = fixed_tasks
    resp_obj1['color'] = "#46BFBD"
    resp_obj1['highlight'] = "#5AD3D1"
    resp_obj1['label'] = "Fixed"
    
    resp_list.append(resp_obj1)
    
    resp_obj2 = {}
    resp_obj2['value'] = invalid_tasks
    resp_obj2['color'] = "#FDB45C"
    resp_obj2['highlight'] = "#FFC870"
    resp_obj2['label'] = "Invalid"
    
    resp_list.append(resp_obj2)
    
    resp_obj3 = {}
    resp_obj3['value'] = wontfix_tasks
    resp_obj3['color'] = "#949FB1"
    resp_obj3['highlight'] = "#A8B3C5"
    resp_obj3['label'] = "Won't fix"
    
    resp_list.append(resp_obj3)
    
    resp_obj4 = {}
    resp_obj4['value'] = duplicate_tasks
    resp_obj4['color'] = "#4D5360"
    resp_obj4['highlight'] = "#616774"
    resp_obj4['label'] = "Duplicate"
    
    resp_list.append(resp_obj4)
    
    resp_obj5 = {}
    resp_obj5['value'] = worksforme_tasks
    resp_obj5['color'] = "#4D5360"
    resp_obj5['highlight'] = "#616774"
    resp_obj5['label'] = "Works for me"
    
    resp_list.append(resp_obj5)
    
    return HttpResponse(json.dumps(resp_list), content_type="application/json")


def eventinfo(request):
    #print(request.GET["pk"])
    
    request_pk = request.GET["pk"]
    event = get_object_or_404(Event,pk=request_pk)
    
    ret_list = []
    
    if event.event_kind == 'C':
        data = {}
        data["name"] = event.commit.hex_sha[:9]
        data["glyph"] = "glyphicon glyphicon-record"
        data["url"] = reverse('commit_detail', args=[event.commit.hex_sha])
        ret_list.append(data)
    elif(event.milestone):
        mstone_dict = {}
        mstone_dict["name"] = event.milestone.name
        mstone_dict["glyph"] = "glyphicon glyphicon-flag"
        mstone_dict["url"] = reverse('mdetail', args=[event.milestone.pk])
        ret_list.append(mstone_dict)
    else:
        try:
            mstone_dict = {}
            mstone_dict["name"] = "{}".format(event.requirement_task.task.name)
            mstone_dict["glyph"] = "glyphicon glyphicon-tasks"
            mstone_dict["url"] = reverse('tdetail', args=[event.requirement_task.task.pk])
            ret_list.append(mstone_dict)
        except:
            pass
        
        try:
            mstone_dict = {}
            mstone_dict["name"] = "{}".format(event.requirement_task.requirement.name)
            mstone_dict["glyph"] = "glyphicon glyphicon-list-alt"
            mstone_dict["url"] = reverse('rdetail', args=[event.requirement_task.requirement.pk])
            ret_list.append(mstone_dict)
        except:
            pass
        
        try:
            mstone_dict = {}
            mstone_dict["name"] = "{}".format(event.requirement_task.task.milestone.name)
            mstone_dict["glyph"] = "glyphicon glyphicon-flag"
            mstone_dict["url"] = reverse('mdetail', args=[event.requirement_task.task.milestone.pk])
            ret_list.append(mstone_dict)
        except:
            pass

    return HttpResponse(json.dumps(ret_list), content_type="application/json")


def userview(request,pk):
    user = get_object_or_404(User,pk=pk)
    tasks_user = Task.objects.filter(assigned_to=user, resolve_type="N")#taskovi na kojima je aktivan korisnik
    
    back = ""
    try:
        back = request.META["HTTP_REFERER"]
    except(KeyError):
        back="/"
    
    context = {"user":user,"back":back, "tasks":tasks_user}
    
    return render(request,"tasks/author.html", context)

def determine_task_state(on_wait, assigned, resolved):
    if resolved:
        return 'Z' # Closed
    elif assigned:
        return 'P' # Accepted
    elif on_wait:
        return 'O' # On wait
    else:
        return 'C' # Created

class TaskUpdate(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name_suffix = '_update_form'
    
    def get_success_url(self):
        return reverse('tdetail',args=(self.get_object().id,))
    
    def form_valid(self, form):
        pk = self.get_object().id
        task = get_object_or_404(Task,pk=pk)
        old_state = get_object_or_404(Task,pk=form.instance.pk).state_kind
        
        form.instance.state_kind = determine_task_state(on_wait=form.cleaned_data.get('is_on_wait'),
                                                   assigned=form.cleaned_data.get('assigned_to'),
                                                   resolved=form.cleaned_data.get('resolve_type') != 'N') # 'N' = Open
        
        response = super(TaskUpdate, self).form_valid(form)
        
        if old_state != form.instance.state_kind:
            StateChange(new_state=form.instance.state_kind, event_user=self.request.user, event_kind='S', date_created=timezone.now(), requirement_task=form.instance).save()
               
        #izmena prioriteta
        priority_var = self.request.POST.get("priority_lvl",None)

        if(priority_var != task.priority_lvl):
            priority_change = PriorityChange(event_user=self.request.user, event_kind="P",
                                       date_created=timezone.now(),requirement_task=form.instance,
                                       milestone=None,new_priority=priority_var)
            priority_change.save()
        
        #izmena resolve-a
        resolve_var = self.request.POST.get("priority_lvl",None)
        
        if(resolve_var != task.resolve_type):
            resolve_change = ResolveEvent(event_user=self.request.user, event_kind="R",
                                       date_created=timezone.now(),requirement_task=form.instance,
                                       milestone=None,new_resolve=resolve_var)
            resolve_change.save()
       
        return response

class TaskCreate(CreateView):
    model = Task
    form_class = TaskCreateForm
    
    def get_success_url(self):
        return reverse('tasks')
    
    def form_valid(self, form):
        form.instance.pub_date = timezone.now()
        form.instance.project_tast_user = self.request.user
        form.instance.state_kind = determine_task_state(on_wait=form.cleaned_data.get('is_on_wait'),
                                                   assigned=form.cleaned_data.get('assigned_to'),
                                                   resolved=False)
        
        # snimi objekat
        resp = super(TaskCreate, self).form_valid(form) 
        
        # snimi dogadjaje
        StateChange(new_state='C', event_user=self.request.user, event_kind='S', date_created=timezone.now(), requirement_task=form.instance).save()
        if  form.instance.state_kind != 'C': # ako je vec promenjeno stanje
            StateChange(new_state=form.instance.state_kind, event_user=self.request.user, event_kind='S', date_created=timezone.now(), requirement_task=form.instance).save()
        
        #add event
        add_req = AddEvent(event_user=self.request.user, event_kind="A",date_created=timezone.now(),
                           requirement_task=form.instance)
        add_req.save()
        
        return resp

def ajax_comment(request, object_type):
    if request.POST:
        content = request.POST.get("content","")
        obj_id = request.POST.get("pk","")
        date = timezone.now()
        milestone=None
        requirement_task=None

        if object_type == Milestone:
            milestone = get_object_or_404(object_type,pk=obj_id)
        else:
            requirement_task = get_object_or_404(object_type,pk=obj_id)

        comment = Comment(event_user=request.user,content=content,
                                  date_created=date,
                                  requirement_task=requirement_task,
                                  milestone=milestone,
                                  event_kind="K")
        comment.save()                                                         
    
    response_data = {}
    response_data['content'] = content
    response_data['date'] = date.__str__()
    response_data['user'] = request.user.username
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def resolve(request):
    
    rid = request.GET["resolveid"]
    box = request.GET["taskid"]
    
    task = get_object_or_404(Task,pk=box)
    task.resolve_type = rid
    task.save()

    """

    if(rid == ""):
        rid = "R"
    
    resolve_change = ResolveEvent(event_user=self.request.user, event_kind="R",
                                       date_created=timezone.now(),requirement_task=task,
                                       milestone=None,new_resolve=rid)
    resolve_change.save()
    """
    
    ret_dict={}
    ret_dict["status"] = "Ok"
    ret_dict["data"] = {}
    ret_dict["code"] = "200"
    
    return HttpResponse(json.dumps(ret_dict), content_type="application/json")

class StatisticsIndexView(TemplateView):
    template_name = 'tasks/statistics.html'
    
    def get_context_data(self, **kwargs):
        context = super(StatisticsIndexView, self).get_context_data(**kwargs)
        context['closed_tasks'] = self.closed_tasks()
        context['created_tasks'] = self.created_tasks()
        context['onwait_tasks'] = self.onwait_tasks()
        context['accepted_tasks'] = self.accepted_tasks()
        context['data'] = self.cycle_time()
        context['lead_time'] = self.lead_time()
        context['average_cycle'] = self.average_cycle_hours()
        context['average_lead'] = self.average_lead_hours()
        context['bar_labels'] = self.get_cycle_labels()
        context['lead_labels'] = self.get_lead_labels()
        context['created'] = self.get_created()
        context['done']=self.get_done()
        context['in_progress']=self.get_in_progress()
        context['onwait'] = self.get_onwait()
        context['date_labels']=self.date_labels()
        return context
    
    def closed_tasks(self):
        closed_tasks = Task.objects.filter(state_kind="Z").count()
        return closed_tasks

    def created_tasks(self):
        created_tasks = Task.objects.filter(state_kind="C").count() 
        return created_tasks
    
    def onwait_tasks(self):
        onwait_tasks = Task.objects.filter(state_kind="O").count()
        return onwait_tasks
    
    def accepted_tasks(self):
        accepted_tasks = Task.objects.filter(state_kind="P").count()
        return accepted_tasks 
    
    def get_hours(self,time):
        return time.total_seconds()/3600;

    def cycle_time(self):   
        data = []        
        closed_tasks = Task.objects.filter(state_kind="Z")
        for i in closed_tasks:  
            accepted = StateChange.objects.filter(requirement_task = i, new_state = "P").exists()
            if accepted:  
                first = StateChange.objects.filter(requirement_task = i, new_state = "P").order_by("date_created").first()            
                latest = StateChange.objects.filter(requirement_task = i, new_state = "Z").order_by("-date_created").first()
                date = latest.date_created - first.date_created
                hours = self.get_hours(date)                
                data.append(round(hours,2))
        return data
    
    def lead_time(self):
        data = []        
        closed_tasks = Task.objects.filter(state_kind="Z")
        for i in closed_tasks:  
            first = StateChange.objects.filter(requirement_task = i, new_state = "C").order_by("date_created").first()
            latest = StateChange.objects.filter(requirement_task = i, new_state = "Z").order_by("-date_created").first()
            date = latest.date_created - first.date_created
            hours = self.get_hours(date)                           
            data.append(round(hours,2))
        return data
           
    def average_cycle_hours(self):
        average = 0
        count_list = []
        closed_tasks = Task.objects.filter(state_kind="Z")
        accepted = StateChange.objects.filter(requirement_task = closed_tasks, new_state = "P")        
        for i in accepted:    
            if i.requirement_task not in count_list:
                count_list.append(i.requirement_task)
        tasks = len(count_list)
        hours = self.cycle_time()
        if tasks != 0:
            average = sum(hours)/tasks
        return round(average,2)
    
    def average_lead_hours(self):
        tasks = Task.objects.filter(state_kind="Z").count()
        hours = self.lead_time()
        average = 0
        if tasks != 0:
            average = sum(hours)/tasks
        return round(average,2)
    
    def get_cycle_labels(self):
        labels = []
        tasks = Task.objects.filter(state_kind="Z")
        for i in tasks:  
            accepted = StateChange.objects.filter(requirement_task = i, new_state = "P")
            for i in accepted:
                lab = i.requirement_task.id
                if lab not in labels:
                    labels.append(lab)    
        return labels
    
    def get_lead_labels(self):
        task = Task.objects.filter(state_kind="Z")
        labels = []
        for t in task:
            labels.append(t.id)
        return labels
    
    def time_interval(self):
        if not Task.objects.all():
            return []
        first = Task.objects.order_by('pub_date').first()
        start = first.pub_date
        end = timezone.now()
        count_days = end - start
        days_number = count_days.days + 2
        date_generated = [start + datetime.timedelta(days=x) for x in range(0,days_number)]
        return date_generated
        
    def get_created(self):
        date_generated = self.time_interval()        
        created = []
        in_progress = []
        done = []
        onwait = []
        list_created = []  
        
        tasks = Task.objects.all()      
        for d in date_generated: 
            z = StateChange.objects.filter(date_created__startswith = d.date, requirement_task = tasks)
            for i in z:
                if i.new_state == "C":
                    created.append(i.requirement_task)
                elif i.new_state == "O":
                    onwait.append(i.requirement_task)
                    if created.__contains__(i.requirement_task):
                        created.remove(i.requirement_task)
                elif i.new_state == "P":
                    in_progress.append(i.requirement_task)
                    if created.__contains__(i.requirement_task):
                        created.remove(i.requirement_task)
                elif i.new_state == "Z":
                    done.append(i.requirement_task)
                    if created.__contains__(i.requirement_task):
                        created.remove(i.requirement_task)
            list_created.append(len(created))        
        return list_created

    def get_onwait(self):
        date_generated = self.time_interval()   
        in_progress = []
        created = []
        done = []
        list_onwait = []
        onwait = []
        
        tasks = Task.objects.all()  
        for d in date_generated:  
            z = StateChange.objects.filter(date_created__startswith = d.date, requirement_task = tasks)
            for i in z:
                if i.new_state == "O":
                    onwait.append(i.requirement_task)
                elif i.new_state == "C":
                    created.append(i.requirement_task)
                    if onwait.__contains__(i.requirement_task):
                        onwait.remove(i.requirement_task)
                elif i.new_state == "P":
                    in_progress.append(i.requirement_task)
                    if onwait.__contains__(i.requirement_task):
                        onwait.remove(i.requirement_task)
                elif i.new_state == "Z":
                    done.append(i.requirement_task)
                    if onwait.__contains__(i.requirement_task):
                        onwait.remove(i.requirement_task)
            list_onwait.append(len(onwait))        
        return list_onwait

    def get_done(self):
        date_generated = self.time_interval()
        created = []
        done = []
        in_progress= []
        list_done = []      
        onwait = []  
        
        tasks = Task.objects.all()  
        for d in date_generated:  
            z = StateChange.objects.filter(date_created__startswith = d.date, requirement_task = tasks)
            for i in z:
                if i.new_state == "Z":
                    done.append(i.requirement_task)
                elif i.new_state == "C":
                    created.append(i.requirement_task)
                    if done.__contains__(i.requirement_task):
                        done.remove(i.requirement_task)
                elif i.new_state == "O":
                    onwait.append(i.requirement_task)
                    if done.__contains__(i.requirement_task):
                        done.remove(i.requirement_task)
                elif i.new_state == "P":
                    in_progress.append(i.requirement_task)
                    if done.__contains__(i.requirement_task):
                        done.remove(i.requirement_task)
            list_done.append(len(done))        
        return list_done  
    
    def get_in_progress(self):
        date_generated = self.time_interval()
        onwait = []
        created = []
        done = []
        in_progress = []
        list_in_progress = []
          
        tasks = Task.objects.all()  
        for d in date_generated:  
            z = StateChange.objects.filter(date_created__startswith = d.date, requirement_task = tasks)
            for i in z:
                if i.new_state == "P":
                    in_progress.append(i.requirement_task)
                elif i.new_state == "C":
                    created.append(i.requirement_task)
                    if in_progress.__contains__(i.requirement_task):
                        in_progress.remove(i.requirement_task)
                elif i.new_state == "O":
                    onwait.append(i.requirement_task)
                    if in_progress.__contains__(i.requirement_task):
                        in_progress.remove(i.requirement_task)
                elif i.new_state == "Z":
                    done.append(i.requirement_task)
                    if in_progress.__contains__(i.requirement_task):
                        in_progress.remove(i.requirement_task)
            list_in_progress.append(len(in_progress))        
        return list_in_progress
    
    def date_labels(self):
        lab = []
        date_generated = self.time_interval()
        for date in date_generated:
            formated = date.strftime('%d-%m-%Y')
            lab.append(formated)
        return lab        
    
