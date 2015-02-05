import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from tasks.forms import MilestoneForm
from tasks.models import Comment, Requirement, Task, StateChange
from tasks.models import Milestone


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


def kanban(request):
    rid = request.GET["id"]
    box = request.GET["box"]
    
    #print("ID:{} BOX:{}".format(rid, box))
    
    #proveri task i kako ga sacuvati
    task = get_object_or_404(Task,pk=rid)
    task.state_kind = box
    
    if(task.state_kind == "P"):
        task.assigned_to = request.user
    
    #promena stanja    
    state_change = StateChange(event_user=request.user, event_kind="S",
                                           date_created=timezone.now(),requirement_task=task,
                                           milestone=task.milestone,new_state=box)
    state_change.save()
    
    task.save()
    
    key_dict ={'C':'#ce2b37','H': '#ee6c3a','M': '#41783f','L': '#3d70b6'}
    
    ret_dict={}
    ret_dict["status"] = "Ok"
    ret_dict["data"] = {}
    ret_dict["code"] = "200"
    ret_dict["message"] = key_dict[task.priority_lvl]
    ret_dict["explaination"]= request.user.username
    
    return HttpResponse(json.dumps(ret_dict), content_type="application/json")