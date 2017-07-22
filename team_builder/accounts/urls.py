from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile_edit/$', views.profile_edit, name='profile_edit'),
]