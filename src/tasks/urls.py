'''
Created on Dec 21, 2014

@author: Milos
'''
from django.conf.urls import patterns, url
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from tasks import views
from tasks.forms import MilestonesList, MilestoneDetail, MilestoneUpdate, \
    RequirementsList, RequirementDetail, RequirementUpdate, RequiremenCreate, \
    TimelineList
from tasks.models import Task, Requirement, Milestone
from tasks.views import TaskUpdate, TaskCreate


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    
    url(r'^milestones/$', MilestonesList.as_view(), name='milestones'),
    url(r'^mdetail/(?P<pk>\d+)/$', MilestoneDetail.as_view(), name='mdetail'),
    url(r'^medit/(?P<pk>\d+)/$', MilestoneUpdate.as_view(), name='medit'),
    url(r'^addmilestone/$', views.addmilestone, name='addmilestone'),
    url(r'^mcomment/$', views.ajax_comment, name='mcomment', kwargs={'object_type':Milestone}),
    
    url(r'^requirements/$', RequirementsList.as_view(), name='requirements'),
    url(r'^rdetail/(?P<pk>\d+)/$', RequirementDetail.as_view(), name='rdetail'),
    url(r'^redit/(?P<pk>\d+)/$', RequirementUpdate.as_view(), name='redit'),
    url(r'^addrequirement/$', RequiremenCreate.as_view(), name='addrequirement'),
    url(r'^rcomment/$', views.ajax_comment, name='rcomment', kwargs={'object_type':Requirement}),
    
    url(r'^kanban/$', views.kanban, name='kanban'),
    url(r'^resolve/$', views.resolve, name='resolve'),
    
    url(r'^timeline/$', TimelineList.as_view(), name='timeline'),
    url(r'^eventinfo/$', views.eventinfo, name='eventinfo'),
    
    url(r'^graph/$', views.testgraph, name='graph'),
    url(r'^prioritygraph/$', views.testgraphpriority, name='prioritygraph'),
    url(r'^resolvegraph/$', views.resolvegraph, name='resolvegraph'),
    
    url(r'^reqgraph/$', views.reqgraph, name='reqgraph'),
    url(r'^reqprioritygraph/$', views.reqtestgraphpriority, name='reqprioritygraph'),
    url(r'^reqresolvegraph/$', views.reqresolvegraph, name='reqresolvegraph'),
    
    url(r'^author/(?P<pk>\d+)/$', views.userview, name='author'),
    
    # tasks
    url(r'^tasks/$', ListView.as_view(model=Task), name='tasks'),
    url(r'^tasks/(?P<pk>\d+)/$', DetailView.as_view(model=Task), name='tdetail'),
    url(r'^tasks/update/(?P<pk>\d+)/$', TaskUpdate.as_view(), name='task_update'),
    url(r'^tasks/create/$', TaskCreate.as_view(), name='task_create'),
    url(r'^task_ajax_comment/$', views.ajax_comment, name='task_ajax_comment', kwargs={'object_type':Task}),
    #url(r'^task_comment/$', views.task_comment, name='task_comment'),
    
    url(r'statistics/$', views.StatisticsIndexView.as_view(), name='statistics'),
)
