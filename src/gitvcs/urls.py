from django.conf.urls import patterns, url

from gitvcs.views import BrowseSourceView, FileContentsView, CommitListView, \
    CommitDetailView, DiffListView, DiffDetailView, DiffSelectView


urlpatterns = patterns('',
    url(r'^browse_source/$', BrowseSourceView.as_view(), name='browse_source'),
    url(r'^browse_source/file/$', FileContentsView.as_view(), name='file_contents'),
    url(r'^diff_select/$', DiffSelectView.as_view(), name='diff_select'),
    url(r'^commits/$', CommitListView.as_view(), name='commit_list'),
    url(r'^commits/(?P<commit>\w+)/$', CommitDetailView.as_view(), name='commit_detail'),
    url(r'^differences/$', DiffListView.as_view(), name='diff_list'),
    url(r'^differences/file/$', DiffDetailView.as_view(), name='diff_detail'),
)