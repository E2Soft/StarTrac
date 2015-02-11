'''
Created on Dec 21, 2014

@author: Milos
'''
"""
    Stranica koja se prikazuje kada korisnik ode na root sajta
    Proverava da li ima autentifikovan korisnik, ako ima samo 
    odradi redirekt na main stranicu tj stranicu tasks aplikacije.
    Ako nije autentifikovan ostavlja stranicu za login kao pocetnu
"""

from django.contrib import auth
from django.shortcuts import render, redirect

from StarTrac.forms import RegistrationForm
from tasks.models import Task


def home(request):
    if request.user.is_authenticated():
        """tasks = Task.objects.order_by('state_kind')
        ret_dict={"O":[],"C":[],"P":[],"Z":[]}
        
        for task in tasks:
            ret_dict[task.state_kind].append(task)
        
        context = {"isadmin":request.user.is_superuser,"username":request.user.username, "tasks":ret_dict}"""
        context = {"isadmin":request.user.is_superuser,"username":request.user.username}

        return render(request,'tasks/logged.html',context)
    else:
        return render(request,'tasks/index.html')

"""
    Login stranica, sa forme uzima username i password koje korisnil
    unese i proverava kroz auth djang-a da li je on u bazi.
    Ako jeste salje dva parametra na render da li je admin i username
    prvo da bi prikazao ili ne link ka admin strani a drugi
    da znamo ko se ulogovao.
    Ako ne postoji ostaje na login strani samo prikazuje poruku o gresci.
    U sablonu je stavljeno csrf_token tako da je taj deo zasticen a 
    render sam po sebi salje taj token
"""    
def login(request):
    if request.user.is_authenticated():
        context = {"isadmin":request.user.is_superuser,"username":request.user.username}
        
        return render(request,'tasks/logged.html',context)
        
    username = request.POST.get("username","")
    password = request.POST.get("password","")
    
    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
        auth.login(request, user)
        context = {"isadmin":user.is_superuser,"username":username}
        
        return render(request,'tasks/logged.html',context)
    else:
        context = {'invalid': "Username and/or password are not ok"}
        return render(request, 'tasks/index.html',context)

"""
    Stranica koja samo vrsi izbacivanje korisnika i vraca na login
    stranicu.Za sve potrebe rada sa korisnicima koristi se 
    djangkov ugradjeni auth sistem da bi izbegli izmisljanje tocka
    ponovo.
"""
def logout(request):
    auth.logout(request)
    return render(request, 'tasks/index.html')

"""
    Stranica koja se bavi registracijom korisnika.Korisiti se ugradjena
    stranica za to od djanga.PRednosti daje prikaz cele forme i moze da se
    bira prikaz, a takodje ima odradjenu validaciju ili bar nesto od iste.
"""
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            context = {'message': "User registred, now login..."}
            return render(request, 'tasks/index.html',context)
        """else:
            print(form.is_valid)
            print(form.error_messages)"""
    else:
        form = RegistrationForm()
    
    back = ""
    try:
        back = request.META["HTTP_REFERER"]
    except(KeyError):
        back = "/"
        
    return render(request,'tasks/register.html', {'form': form,"back":back})