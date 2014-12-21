from django.conf.urls import patterns, include, url
from django.contrib import admin

from src.StarTrac import views


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'StarTrac.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^tasks/', include('tasks.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'login/', views.login, name='login'),
    url(r'logout/', views.logout, name='logout'),
)
