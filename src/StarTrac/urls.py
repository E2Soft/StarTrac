from django.conf.urls import patterns, include, url
from django.contrib import admin

from StarTrac import views
from StarTrac.forms import UserUpdate, DetailUser, UserCreate


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'StarTrac.views.home', name='home'),
    url(r'^', include('tasks.urls')),
    url(r'^git/', include('gitvcs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'login/', views.login, name='login'),
    url(r'logout/', views.logout, name='logout'),
    url(r'register/', UserCreate.as_view(), name='register'),
    url(r'uedit/(?P<pk>\d+)/$', UserUpdate.as_view(), name='uedit'),
    url(r'^udetail/$', DetailUser.as_view(), name='udetail'),
)
