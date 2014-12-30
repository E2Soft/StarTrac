'''
Created on Dec 21, 2014

@author: Milos
'''
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False)
    
    class Meta:
        model = User
        fields = ['first_name','last_name', 'username', 'email', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

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