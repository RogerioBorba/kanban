from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from hyper_resource.views import *
from scrum.models import *
from scrum.serializers import *
from scrum.contexts import *

def get_root_response(request):
    format = None
    root_links = {

      'continuous-activity-list': reverse('scrum:ContinuousActivity_list' , request=request, format=format),
      'impediment-list': reverse('scrum:Impediment_list' , request=request, format=format),
      'project-list': reverse('scrum:Project_list' , request=request, format=format),
      'scrum-user-list': reverse('scrum:ScrumUser_list' , request=request, format=format),
      'sprint-list': reverse('scrum:Sprint_list' , request=request, format=format),
      'task-list': reverse('scrum:Task_list' , request=request, format=format),
    }

    ordered_dict_of_link = OrderedDict(sorted(root_links.items(), key=lambda t: t[0]))
    return ordered_dict_of_link

class APIRoot(APIView):

    def __init__(self):
        super(APIRoot, self).__init__()
        self.base_context = BaseContext('api-root')

    def options(self, request, *args, **kwargs):
        context = self.base_context.getContextData(request)
        root_links = get_root_response(request)
        context.update(root_links)
        response = Response(context, status=status.HTTP_200_OK, content_type="application/ld+json")
        response = self.base_context.addContext(request, response)
        return response

    def get(self, request, *args, **kwargs):
        root_links = get_root_response(request)
        response = Response(root_links)
        return self.base_context.addContext(request, response)

class ContinuousActivityList(CollectionResource):
    queryset = ContinuousActivity.objects.all()
    serializer_class = ContinuousActivitySerializer
    contextclassname = 'continuous-activity-list'
    def initialize_context(self):
        self.context_resource = ContinuousActivityContext()
        self.context_resource.resource = self

class ContinuousActivityDetail(NonSpatialResource):
    serializer_class = ContinuousActivitySerializer
    contextclassname = 'continuous-activity-list'
    def initialize_context(self):
        self.context_resource = ContinuousActivityContext()
        self.context_resource.resource = self

class ImpedimentList(CollectionResource):
    queryset = Impediment.objects.all()
    serializer_class = ImpedimentSerializer
    contextclassname = 'impediment-list'
    def initialize_context(self):
        self.context_resource = ImpedimentContext()
        self.context_resource.resource = self

class ImpedimentDetail(NonSpatialResource):
    serializer_class = ImpedimentSerializer
    contextclassname = 'impediment-list'
    def initialize_context(self):
        self.context_resource = ImpedimentContext()
        self.context_resource.resource = self

class ProjectList(CollectionResource):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    contextclassname = 'project-list'
    def initialize_context(self):
        self.context_resource = ProjectContext()
        self.context_resource.resource = self

class ProjectDetail(NonSpatialResource):
    serializer_class = ProjectSerializer
    contextclassname = 'project-list'
    def initialize_context(self):
        self.context_resource = ProjectContext()
        self.context_resource.resource = self

class ScrumUserList(CollectionResource):
    queryset = ScrumUser.objects.all()
    serializer_class = ScrumUserSerializer
    contextclassname = 'user-list'
    def initialize_context(self):
        self.context_resource = ScrumUserContext()
        self.context_resource.resource = self

class ScrumUserRegister(CollectionResource):
    queryset = ScrumUser.objects.all()
    serializer_class = ScrumUserSerializer
    contextclassname = 'user-list'
    def initialize_context(self):
        self.context_resource = ScrumUserContext()
        self.context_resource.resource = self

    def post(self, request, *args, **kwargs):
        #print(request)
        resp = super(ScrumUserRegister, self).post(request, *args, **kwargs)
        resp['x-access-token'] = self.object_model.getToken()
        return resp

class ScrumUserLogin(CollectionResource):
    queryset = ScrumUser.objects.all()
    serializer_class = ScrumUserSerializer
    contextclassname = 'user-list'
    def initialize_context(self):
        self.context_resource = ScrumUserContext()
        self.context_resource.resource = self

    def post(self, request, *args, **kwargs):

        res = ScrumUser.getOneOrNone(request.data['user_name'], request.data['password'])

        if res is None:
            res = Response(status=status.HTTP_401_UNAUTHORIZED, content_type='application/json')
            res['WWW-Authenticate'] = 'Bearer'
            return res
        response = Response(status=status.HTTP_201_CREATED, content_type='application/json')
        response['Content-Location'] = request.path + str(res.id) + '/'
        response['x-access-token'] = res.getToken()
        return response

class ScrumUserDetail(NonSpatialResource):
    serializer_class = ScrumUserSerializer
    contextclassname = 'user-list'
    def initialize_context(self):
        self.context_resource = ScrumUserContext()
        self.context_resource.resource = self

class SprintList(CollectionResource):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    contextclassname = 'sprint-list'
    def initialize_context(self):
        self.context_resource = SprintContext()
        self.context_resource.resource = self

class SprintDetail(NonSpatialResource):
    serializer_class = SprintSerializer
    contextclassname = 'sprint-list'
    def initialize_context(self):
        self.context_resource = SprintContext()
        self.context_resource.resource = self

class TaskList(CollectionResource):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    contextclassname = 'task-list'
    def initialize_context(self):
        self.context_resource = TaskContext()
        self.context_resource.resource = self

class TaskListStatus(CollectionResource):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    contextclassname = 'task-list'
    def initialize_context(self):
        self.context_resource = TaskContext()
        self.context_resource.resource = self

    def get(self, request, *args, **kwargs):
       a_data = Task.status_dic()
       return Response(data=a_data, content_type='application/json')

class TaskDetail(NonSpatialResource):
    serializer_class = TaskSerializer
    contextclassname = 'task-list'
    def initialize_context(self):
        self.context_resource = TaskContext()
        self.context_resource.resource = self

class ContinuousActivityTypeList(CollectionResource):
    queryset = ContinuousActivity.objects.all()
    serializer_class = ContinuousActivitySerializer
    contextclassname = 'continuous-activity-list'
    def initialize_context(self):
        self.context_resource = ContinuousActivityContext()
        self.context_resource.resource = self

    def get(self, request, *args, **kwargs):
       a_data = ContinuousActivity.type_dic()
       return Response(data=a_data, content_type='application/json')
