import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.edit import UpdateView, CreateView

from tasks.forms import MilestoneForm, TaskUpdateForm, TaskCreateForm
from tasks.models import Task, Milestone, Comment, Requirement, StateChange, \
    Event
from django.contrib.auth.decorators import login_required


    # Create your views here.
def index(request):
    if request.user.is_authenticated():
        tasks = Task.objects.order_by('state_kind')
        ret_dict={"O":[],"C":[],"P":[],"Z":[]}
        
        for task in tasks:
            ret_dict[task.state_kind].append(task)
        
        context = {"isadmin":request.user.is_superuser,"username":request.user.username, "tasks":ret_dict}
        
        return render(request,'tasks/logged.html',context)
    else:
        return render(request,'tasks/index.html')

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
def addmilestone(request):
    if request.POST:
        form = MilestoneForm(request.POST)
        if form.is_valid():
            form.instance.date_created = timezone.now()
            form.save()
            
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


@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
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
    
@login_required(login_url="/login/")    
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
    
@login_required(login_url="/login/")    
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

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
def eventinfo(request):
    #print(request.GET["pk"])
    
    request_pk = request.GET["pk"]
    event = get_object_or_404(Event,pk=request_pk)
    
    ret_list = []
    
    if(event.milestone):
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

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
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

        old_state = get_object_or_404(Task,pk=form.instance.pk).state_kind
        
        form.instance.state_kind = determine_task_state(on_wait=form.cleaned_data.get('is_on_wait'),
                                                   assigned=form.cleaned_data.get('assigned_to'),
                                                   resolved=form.cleaned_data.get('resolve_type') != 'N') # 'N' = Open
        
        response = super(TaskUpdate, self).form_valid(form)
        
        if old_state != form.instance.state_kind:
            StateChange(new_state=form.instance.state_kind, event_user=self.request.user, event_kind='S', date_created=timezone.now(), requirement_task=form.instance).save()
        
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
    
        return super(TaskCreate, self).form_valid(form)
    
@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
def resolve(request):
    
    rid = request.GET["resolveid"]
    box = request.GET["taskid"]
    
    task = get_object_or_404(Task,pk=box)
    task.resolve_type = rid
    task.save()
    
    #print("bla bla {} {}".format(rid, box))
    
    ret_dict={}
    ret_dict["status"] = "Ok"
    ret_dict["data"] = {}
    ret_dict["code"] = "200"
    
    return HttpResponse(json.dumps(ret_dict), content_type="application/json")


