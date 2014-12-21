from django.shortcuts import render

# Create your views here.
def index(request):
    if request.user.is_authenticated():
        context = {"isadmin":request.user.is_superuser,"username":request.user.username}
        
        return render(request,'tasks/logged.html',context)
    else:
        return render(request,'tasks/index.html')