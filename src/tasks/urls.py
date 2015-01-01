'''
Created on Dec 21, 2014

@author: Milos
'''
from django.conf.urls import patterns, url

from tasks import views
from tasks.forms import MilestonesList, MilestoneDetail, MilestoneUpdate, \
    RequirementsList, RequirementDetail, RequirementUpdate, RequiremenCreate


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^milestones/$', MilestonesList.as_view(), name='milestones'),
    url(r'^mdetail/(?P<pk>\d+)/$', MilestoneDetail.as_view(), name='mdetail'),
    url(r'^mcomment/$', views.mcomment, name='mcomment'),
    url(r'^medit/(?P<pk>\d+)/$', MilestoneUpdate.as_view(), name='medit'),
    url(r'^addmilestone/$', views.addmilestone, name='addmilestone'),
    url(r'^requirements/$', RequirementsList.as_view(), name='requirements'),
    url(r'^rdetail/(?P<pk>\d+)/$', RequirementDetail.as_view(), name='rdetail'),
    url(r'^redit/(?P<pk>\d+)/$', RequirementUpdate.as_view(), name='redit'),
    url(r'^addrequirement/$', RequiremenCreate.as_view(), name='addrequirement'),
     url(r'^rcomment/$', views.rcomment, name='rcomment'),
)