'''
Created on Dec 21, 2014

@author: Milos
'''
from django.contrib import auth
from django.shortcuts import render

"""
    Stranica koja se prikazuje kada korisnik ode na root sajta
    Proverava da li ima autentifikovan korisnik, ako ima samo 
    odradi redirekt na main stranicu tj stranicu tasks aplikacije.
    Ako nije autentifikovan ostavlja stranicu za login kao pocetnu
"""
def home(request):
    if request.user.is_authenticated():
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