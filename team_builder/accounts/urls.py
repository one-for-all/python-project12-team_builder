from django.conf.urls import url

from . import views
from . import endpoints


urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile_edit/$', views.profile_edit, name='profile_edit'),
    url(r'^profile/(?P<username>[_\d\w]+)/$', views.profile_other,
        name='profile_other'),
    # Endpoints
    url(r'^api/v1/signup/$', endpoints.signup, name='api_signup'),
    url(r'^api/v1/login/$', endpoints.login_user, name='api_login'),
    url(r'^api/v1/logout/$', endpoints.logout_user, name='api_logout'),
    url(r'^api/v1/profile/$', endpoints.profile, name='api_profile'),
    url(r'^api/v1/profile/(?P<username>[_\w]+)/$', endpoints.profile_other,
        name='api_profile_other'),

]