from rest_framework import serializers

from hyper_resource.serializers import BusinessSerializer
from scrum.models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from rest_framework.serializers import ModelSerializer, HyperlinkedRelatedField


class TypeContinuousActivitySerializer(BusinessSerializer):

    class Meta:
        model = TypeContinuousActivity
        fields = ['id','name','type']
        identifier = 'id'
        identifiers = ['pk', 'id']



class ContinuousActivitySerializer(BusinessSerializer):
    responsible = HyperlinkedRelatedField(view_name='scrum:ScrumUser_detail', many=False, read_only=True)
    typeContinuousActivity = HyperlinkedRelatedField(view_name='scrum:TypeContinuousActivity_detail', many=False, read_only=True)
    class Meta:
        model = ContinuousActivity
        fields = ['id','name','description', 'responsible','typeContinuousActivity','started', 'ended']
        identifier = 'id'
        identifiers = ['pk', 'id']

    def field_relationship_to_validate_dict(self):
        a_dict = {}
        a_dict['responsible_id'] = 'responsible'
        a_dict['typeContinuousActivity_id'] = 'typeContinuousActivity'
        return a_dict


class ImpedimentSerializer(ModelSerializer):
    sprint = HyperlinkedRelatedField(view_name='scrum:Sprint_detail', many=False, read_only=True)
    task = HyperlinkedRelatedField(view_name='scrum:Task_detail', many=False, read_only=True)
    class Meta:
        model = Impediment
        fields = ['id','name','description','created_date','resolution_date','sprint','task']
        identifier = 'id'
        identifiers = ['pk', 'id']

    def get_id_relationship_from_request(self, field_name_relationship):
        if field_name_relationship not in self.initial_data:
            return None
        field_iri = self.initial_data[field_name_relationship]
        if field_iri != None and field_iri != '':
            arr = field_iri.split('/')
            return  arr[-1] if arr[-1] != '' else arr[-2]
        return None

    def field_relationship_to_validate_dict(self):
        a_dict = {}
        a_dict['sprint_id'] = 'sprint'
        a_dict['task_id'] = 'task'

    def transform_relationship_from_request(self, validated_data):
        for key, value in self.field_relationship_to_validate_dict():
             validated_data[key] = self.get_id_relationship_from_request(value)

    def create_or_update(self, instance, validated_data):
        an_instance = instance
        self.transform_relationship_from_request(validated_data)
        if an_instance is None:
            an_instance = super(ImpedimentSerializer, self).create(validated_data)
        else:
            an_instance = super(ImpedimentSerializer, self).update(instance, validated_data)

        return an_instance

    def create(self, validated_data):
        return self.create_or_update(None, validated_data)

    def update(self, instance, validated_data):
        return self.create_or_update(instance, validated_data)

class ProjectSerializer(ModelSerializer):
    tasks = HyperlinkedRelatedField(view_name='scrum:Task_detail', many=True, read_only=True)
    sprints = HyperlinkedRelatedField(view_name='scrum:Sprint_detail', many=True, read_only=True)
    technical_responsible = HyperlinkedRelatedField(view_name='scrum:ScrumUser_detail', many=False, read_only=True)
    administrative_responsible = HyperlinkedRelatedField(view_name='scrum:ScrumUser_detail', many=False, read_only=True)
    class Meta:
        model = Project
        fields = ['tasks','id','name','description','start','end','technical_responsible', 'administrative_responsible', 'sprints']
        identifier = 'id'
        identifiers = ['pk', 'id']

    def get_id_relationship_from_request(self, field_name_relationship):
        if field_name_relationship not in self.initial_data:
            return None
        field_iri = self.initial_data[field_name_relationship]
        if field_iri != None and field_iri != '':
            arr = field_iri.split('/')
            return  arr[-1] if arr[-1] != '' else arr[-2]
        return None

    def transform_relationship_from_request(self, validated_data):
        validated_data['technical_responsible_id'] = self.get_id_relationship_from_request('technical_responsible')
        validated_data['administrative_responsible_id'] = self.get_id_relationship_from_request( 'administrative_responsible')

    def create_or_update(self, instance, validated_data):
        an_instance = instance
        self.transform_relationship_from_request(validated_data)
        if an_instance is None:
            an_instance = super(ProjectSerializer, self).create(validated_data)
        else:
            an_instance = super(ProjectSerializer, self).update(instance, validated_data)
        an_instance.technical_responsible_id = validated_data['technical_responsible_id']
        an_instance.administrative_responsible_id = validated_data['administrative_responsible_id']
        return an_instance

    def create(self, validated_data):
        return self.create_or_update(None, validated_data)

    def update(self, instance, validated_data):
        return self.create_or_update(instance, validated_data)

class ScrumUserSerializer(ModelSerializer):
    continuous_activities = HyperlinkedRelatedField(view_name='scrum:ContinuousActivity_detail', many=True, read_only=True)
    sprints = HyperlinkedRelatedField(view_name='scrum:Sprint_detail', many=True, read_only=True)
    tasks = HyperlinkedRelatedField(view_name='scrum:Task_detail', many=True, read_only=True)
    class Meta:
        model = ScrumUser
        fields = ['continuous_activities','sprints','tasks','id','name','user_name','email', 'description','role', 'password']
        identifier = 'id'
        identifiers = ['pk', 'id']


class SprintSerializer(BusinessSerializer):
    project = HyperlinkedRelatedField(view_name='scrum:Project_detail', many=False, read_only=True)
    tasks = HyperlinkedRelatedField(view_name='scrum:Task_detail', many=True, read_only=True)
    impediments = HyperlinkedRelatedField(view_name='scrum:Impediment_detail', many=True, read_only=True)
    responsible = HyperlinkedRelatedField(view_name='scrum:ScrumUser_detail', many=False, read_only=True)
    class Meta:
        model = Sprint
        fields = ['tasks','impediments','id','code','start','end','responsible', 'project']
        identifier = 'id'
        identifiers = ['pk', 'id']

    def field_relationship_to_validate_dict(self):
        a_dict = {}
        a_dict['responsible_id'] = 'responsible'
        a_dict['project_id'] = 'project'
        return a_dict

class TaskSerializer(BusinessSerializer):
    impediments = HyperlinkedRelatedField(view_name='scrum:Impediment_detail', many=True, read_only=True)
    sprint = HyperlinkedRelatedField(view_name='scrum:Sprint_detail', many=False, read_only=True)
    responsible = HyperlinkedRelatedField(view_name='scrum:ScrumUser_detail', many=False, read_only=True)
    project = HyperlinkedRelatedField(view_name='scrum:Project_detail', many=False, read_only=True)
    typeContinuousActivity = HyperlinkedRelatedField(view_name='scrum:TypeContinuousActivity_detail', many=False,
                                                     read_only=True)
    to_string = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['to_string',  'impediments','id','name','description','status','order','started','due','completed','sprint','responsible','typeContinuousActivity','project']
        identifier = 'id'
        identifiers = ['pk', 'id']

    def field_relationship_to_validate_dict(self):
        a_dict = {}
        a_dict['project_id'] = 'project' #task.project.id = project
        a_dict['sprint_id'] = 'sprint'
        a_dict['responsible_id'] = 'responsible'
        a_dict['typeContinuousActivity_id'] = 'typeContinuousActivity'
        return a_dict

    def to_string(self, obj):
        return obj.to_string()

