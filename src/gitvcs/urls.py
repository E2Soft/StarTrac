from django.conf.urls import patterns, url
from gitvcs import views


urlpatterns = patterns('',
    url(r'^test/$', views.test, name='test'),
    url(r'^branches/$', views.branches_list, name='branches_list'),
)