from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/register/complete/$', views.registration_complete, name='registration_complete'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', { 'template_name': 'registration/loggedout.html',}, name='logout',),
    url(r'^accounts/loggedin/$', views.loggedin, name='loggedin'),
    url(r'^administration/$', views.administration, name='administration'),
    url(r'^finduser/$', views.finduser, name='finduser'),
    url(r'^friendshiprequests/$', views.friendshiprequestslist, name='friendshiprequests'),
    url(r'^myfriends/$', views.myfriends, name='myfriends'),
    url(r'^connections/$', views.connections, name='connections'),
]
