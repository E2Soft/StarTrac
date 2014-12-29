'''
Created on Dec 21, 2014

@author: Milos
'''
from django.conf.urls import patterns, url

from src.tasks import views
from tasks.forms import MilestonesList


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^milestones/$', MilestonesList.as_view(), name='milestones'),
)