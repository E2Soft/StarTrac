from django.conf.urls import patterns, url

from gitvcs import views
from gitvcs.views import BrowseSourceView, FileContentsView, CommitListView


urlpatterns = patterns('',
    url(r'^browse_source/$', BrowseSourceView.as_view(), name='browse_source'),
    url(r'^browse_source/file/$', FileContentsView.as_view(), name='file_contents'),
    url(r'^diff/$', views.diff, name='diff'),
    url(r'^commit_list/$', CommitListView.as_view(), name='commit_list'),
)