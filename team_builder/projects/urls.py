from django.conf.urls import url

from . import views
from . import endpoints

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^new', views.new_project, name='new'),
    url(r'^(?P<pk>\d+)/$', views.view_project, name='view'),
    url(r'^edit/(?P<pk>\d+)/$', views.edit_project, name='edit'),
    # Endpoints
    url(r'^api/v1/projects/$', endpoints.project_list, name='api_list'),
    url(r'^api/v1/project/(?P<pk>\d+)/$', endpoints.project,
        name='api_detail'),
]
