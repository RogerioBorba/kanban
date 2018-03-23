from django.conf.urls import include, url
urlpatterns = [

    url(r'^scrum-list/',include('scrum.urls',namespace='scrum')),


]
urlpatterns += [

    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),

]


