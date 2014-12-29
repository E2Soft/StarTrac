import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from tasks.models import Comment
from tasks.models import Milestone


# Create your views here.
def index(request):
    if request.user.is_authenticated():
        context = {"isadmin":request.user.is_superuser,"username":request.user.username}
        
        return render(request,'tasks/logged.html',context)
    else:
        return render(request,'tasks/index.html')
    
def mcomment(request):
    if request.POST:
        ccontent = request.POST.get("content","")
        milestone_id = request.POST.get("pk","")
        date = timezone.now()
        milestone = get_object_or_404(Milestone,pk=milestone_id)
        
        
        comment = Comment(event_user=request.user,content=ccontent,
                                  date_created=date,
                                  milestone=milestone,event_kind="K")
        comment.save()                                                         
    
    response_data = {}
    response_data['content'] = 'ccontent'
    response_data['date'] = date.__str__()
    response_data['user'] = request.user.username
    return HttpResponse(json.dumps(response_data), content_type="application/json")