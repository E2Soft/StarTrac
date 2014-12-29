import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

import tasks
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
        content = request.POST.get("content","")
        milestone_id = request.POST.get("pk","")
        date = timezone.now()
        milestone = get_object_or_404(Milestone,pk=milestone_id)
        
        """print("stigo post params: {}, {}, {}, {}, {}, {}, {}".format(hello, content, milestone_id, 
                                                                 date, milestone, request.user, "K"))"""
    
    response_data = {}
    response_data['result'] = 'failed'
    response_data['message'] = 'You messed up'
    return HttpResponse(json.dumps(response_data), content_type="application/json")