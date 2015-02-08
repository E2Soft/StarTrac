'''
Created on Dec 21, 2014

@author: Milos
'''
from django.conf.urls import patterns, url

from tasks import views
from tasks.forms import MilestonesList, MilestoneDetail, MilestoneUpdate, \
    RequirementsList, RequirementDetail, RequirementUpdate, RequiremenCreate, \
    TimelineList
from tasks.views import TaskList, TaskDetail, TaskUpdate, TaskCreate


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    
    url(r'^milestones/$', MilestonesList.as_view(), name='milestones'),
    url(r'^mdetail/(?P<pk>\d+)/$', MilestoneDetail.as_view(), name='mdetail'),
    url(r'^medit/(?P<pk>\d+)/$', MilestoneUpdate.as_view(), name='medit'),
    url(r'^addmilestone/$', views.addmilestone, name='addmilestone'),
    url(r'^mcomment/$', views.mcomment, name='mcomment'),
    
    url(r'^requirements/$', RequirementsList.as_view(), name='requirements'),
    url(r'^rdetail/(?P<pk>\d+)/$', RequirementDetail.as_view(), name='rdetail'),
    url(r'^redit/(?P<pk>\d+)/$', RequirementUpdate.as_view(), name='redit'),
    url(r'^addrequirement/$', RequiremenCreate.as_view(), name='addrequirement'),
    url(r'^rcomment/$', views.rcomment, name='rcomment'),
    
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
    url(r'^tasks/$', TaskList.as_view(), name='tasks'),
    url(r'^tasks/(?P<pk>\d+)/$', TaskDetail.as_view(), name='task_detail'),
    url(r'^tasks/update/(?P<pk>\d+)/$', TaskUpdate.as_view(), name='task_update'),
    url(r'^tasks/create/$', TaskCreate.as_view(), name='task_create'),
    #url(r'^task_comment/$', views.task_comment, name='task_comment'),
)