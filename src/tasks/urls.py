'''
Created on Dec 21, 2014

@author: Milos
'''
from django.conf.urls import patterns, url

from src.tasks import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)