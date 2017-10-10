from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from scrum import views 

urlpatterns = format_suffix_patterns([
    url(r'^$', views.APIRoot.as_view(), name='api_root'),
    url(r'^continuous-activity-list/type-dominio-list/(?P<pk>[0-9]+)/?$', views.ContinuousActivityTypeList.as_view(), name='Task_list_af'),
    url(r'^continuous-activity-list/(?P<pk>[0-9]+)/$', views.ContinuousActivityDetail.as_view(), name='ContinuousActivity_detail'),
    url(r'^continuous-activity-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/$', views.ContinuousActivityDetail.as_view(), name='ContinuousActivity_detail_af'),
    url(r'^continuous-activity-list/$', views.ContinuousActivityList.as_view(), name='ContinuousActivity_list'),
    url(r'^continuous-activity-list/type-dominio-list/?$', views.ContinuousActivityTypeList.as_view(), name='ContinuousActivity_list'),
    url(r'^continuous-activity-list/(?P<attributes_functions>.*)/?$', views.ContinuousActivityList.as_view(), name='ContinuousActivity_list_af'),

    url(r'^impediment-list/(?P<pk>[0-9]+)/$', views.ImpedimentDetail.as_view(), name='Impediment_detail'),
    url(r'^impediment-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/$', views.ImpedimentDetail.as_view(), name='Impediment_detail_af'),
    url(r'^impediment-list/$', views.ImpedimentList.as_view(), name='Impediment_list'),
    url(r'^impediment-list/(?P<attributes_functions>.*)/?$', views.ImpedimentList.as_view(), name='Impediment_list_af'),

    url(r'^project-list/(?P<pk>[0-9]+)/$', views.ProjectDetail.as_view(), name='Project_detail'),
    url(r'^project-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/$', views.ProjectDetail.as_view(), name='Project_detail_af'),
    url(r'^project-list/$', views.ProjectList.as_view(), name='Project_list'),
    url(r'^project-list/(?P<attributes_functions>.*)/?$', views.ProjectList.as_view(), name='Project_list_af'),

    url(r'^scrum-user-list/(?P<pk>[0-9]+)/$', views.ScrumUserDetail.as_view(), name='ScrumUser_detail'),
    url(r'^scrum-user-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/$', views.ScrumUserDetail.as_view(), name='ScrumUser_detail_af'),
    url(r'^scrum-user-list/$', views.ScrumUserList.as_view(), name='ScrumUser_list'),
    url(r'^scrum-user-list/(?P<attributes_functions>.*)/?$', views.ScrumUserList.as_view(), name='ScrumUser_list_af'),

    url(r'^sprint-list/(?P<pk>[0-9]+)/$', views.SprintDetail.as_view(), name='Sprint_detail'),
    url(r'^sprint-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/$', views.SprintDetail.as_view(), name='Sprint_detail_af'),
    url(r'^sprint-list/$', views.SprintList.as_view(), name='Sprint_list'),
    url(r'^sprint-list/(?P<attributes_functions>.*)/?$', views.SprintList.as_view(), name='Sprint_list_af'),

    url(r'^task-list/status-dominio-list/(?P<pk>[0-9]+)/?$', views.TaskListStatus.as_view(), name='Task_list_af'),
    url(r'^task-list/(?P<pk>[0-9]+)/$', views.TaskDetail.as_view(), name='Task_detail'),
    url(r'^task-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/$', views.TaskDetail.as_view(), name='Task_detail_af'),
    url(r'^task-list/$', views.TaskList.as_view(), name='Task_list'),
    url(r'^task-list/status-dominio-list/?$', views.TaskListStatus.as_view(), name='Task_list_af'),
    url(r'^task-list/(?P<attributes_functions>.*)/?$', views.TaskList.as_view(), name='Task_list_af'),


])
