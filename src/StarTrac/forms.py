'''
Created on Dec 21, 2014

@author: Milos
'''
'''
Forma za eventualna prosirenja djangovog user-a
'''

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView

from tasks.models import UserExtend


class UserExtendForm(forms.ModelForm):
    class Meta:
        model = UserExtend
        fields = ['picture']
        
        

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False)
    
    class Meta:
        model = UserExtend
        fields = ['first_name','last_name', 'username', 'email', 'password1', 'password2','picture']
        
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.picture = self.cleaned_data['picture']

        if commit:
            user.save()

        return user
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs['class']='form-control'
        self.fields["last_name"].widget.attrs['class']='form-control'
        self.fields["username"].widget.attrs['class']='form-control'
        self.fields["email"].widget.attrs['class']='form-control'
        self.fields["password1"].widget.attrs['class']='form-control'
        self.fields["password2"].widget.attrs['class']='form-control'
        self.fields["picture"].widget.attrs['class']='form-control'

class UserForm(forms.ModelForm):
    class Meta:
        model = UserExtend
        fields = ['first_name','last_name', 'username', 'email', 'picture']
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs['class']='form-control'
        self.fields["last_name"].widget.attrs['class']='form-control'
        self.fields["username"].widget.attrs['class']='form-control'
        self.fields["email"].widget.attrs['class']='form-control'
        self.fields["picture"].widget.attrs['class']='form-control'

class UserCreate(CreateView):
    model = UserExtend
    template_name = 'tasks/register.html'
    form_class = RegistrationForm
    
    def get_success_url(self):
        return reverse('home')
    
    def get_context_data(self, **kwargs):
        context = super(UserCreate, self).get_context_data(**kwargs)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
     
        return context
        
class UserUpdate(UpdateView):
    model = UserExtend
    template_name = 'tasks/uupdate.html'
    form_class = UserForm
    
    def get_success_url(self):
        return reverse('udetail')
    
    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
     
        return context
    
class DetailUser(DetailView):
    model = UserExtend
    template_name = 'tasks/udetail.html'
    context_object_name='user'
    
    
    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)
    
    def get_context_data(self, **kwargs):
        context = super(DetailUser, self).get_context_data(**kwargs)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
        
        #context["user"] = self.request.user
        return context