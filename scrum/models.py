from __future__ import unicode_literals

import base64

import jwt

from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
from datetime import datetime
from django.db import models

# Create your models here.
from hyper_resource.models import BusinessModel
from kanban.settings import SECRET_KEY


class ScrumUser(BusinessModel):
    contextclassname = 'user-list'
    name = models.CharField(max_length=100, blank=True, default='')
    user_name = models.CharField(max_length=100, unique=True )
    email = models.CharField(max_length=100, unique=True, null=True)
    password  = models.CharField(max_length=100, unique=True )
    description = models.TextField(blank=True, null=True, default='')
    role = models.CharField(max_length=100, blank=True, default='user')
    avatar = models.CharField(max_length=200, blank=True, default='')
    active   = models.NullBooleanField()

    @classmethod
    def jwt_algorithm(cls):
        return 'HS256'

    @classmethod
    def getOneOrNone(cls, a_user_name, password):
        return ScrumUser.objects.filter(user_name=a_user_name, password=password).first()

    def getToken(self):
        encoded = jwt.encode({'id': self.id, 'user_name': self.user_name, 'avatar': self.avatar}, SECRET_KEY,
                             algorithm=ScrumUser.jwt_algorithm())
        return encoded

    @classmethod
    def login(cls, user_name, password):
        user = ScrumUser.getOneOrNone(user_name, password)
        if user is None:
            return None
        a_dict = {}
        a_dict['id'] = user.id
        a_dict['name'] = user.name
        a_dict['user_name'] = user.user_name
        a_dict['avatar'] = user.avatar
        a_dict['token'] = user_name.getToken()
        return a_dict

    @classmethod
    def token_is_ok(cls, a_token):
        try:
            payload = jwt.decode(a_token, SECRET_KEY, algorithm=ScrumUser.jwt_algorithm())
            return True
        except jwt.InvalidTokenError:
            return False

    def encodeField(self, a_field):
        return base64.b64encode(a_field.encode())

    def decodeField(self, a_field):
        return base64.b64decode(a_field.encode())

class ContinuousActivity(BusinessModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, default='')
    type = models.IntegerField(blank=True, null=True, default='')
    responsible = models.ForeignKey(ScrumUser,  db_column='id_scrumuser',related_name='continuous_activities', blank=True, null=True)
    started = models.DateField(null=True,blank=True)
    ended = models.DateField(null=True,blank=True)
    TYPE_COMMITTEE = 1
    TYPE_MEETING = 2
    TYPE_COLLABORATIVE_WORK = 3
    TYPE_CHOICES = (
        (TYPE_COMMITTEE, ('Comitê')),
        (TYPE_MEETING, ('Reunião')),
        (TYPE_COLLABORATIVE_WORK, ('Trabalho colaborativo')),
    )

    @classmethod
    def type_dic(cls):
        dic_values = [ ]
        for tupla in cls.TYPE_CHOICES:
            dicti = {}
            dicti['id'] = tupla[0]
            dicti['dominio'] = tupla[1]
            dic_values.append(dicti)
        return dic_values

class Project(BusinessModel):
    name = models.CharField(max_length=100 )
    description = models.TextField(blank=True, null=True, default='')
    start = models.DateField(null=True,blank=True)
    real_start = models.DateField(null=True,blank=True)
    end = models.DateField(null=True, blank=True)
    real_end = models.DateField(null=True, blank=True)
    technical_responsible = models.ForeignKey(ScrumUser,  db_column='id_scrumuser_technical',related_name='projects', blank=True, null=True)
    administrative_responsible = models.ForeignKey(ScrumUser,  db_column='id_scrumuser_administrative', blank=True, null=True)


class Sprint(BusinessModel):
    contextclassname = 'sprints'
    id = models.AutoField(primary_key=True, db_column='id_sprint')
    code = models.CharField(max_length=100 )
    #description = models.TextField(blank=True, null=True, default='')
    start = models.DateField(null=True,blank=True)
    end = models.DateField(null=True, blank=True)
    #real_end = models.DateField(null=True, blank=True)
    responsible = models.ForeignKey(ScrumUser,  db_column='id_scrumuser',related_name='sprints', blank=True, null=True)
    project = models.ForeignKey(Project,  db_column='id_project',related_name='sprints', blank=True, null=True)

    def __str__(self):
        return self.name or ('Sprint ending %s') % self.end

class Task(BusinessModel):
    contextclassname = 'tasks'
    #Unit of work to be done for the sprint
    STATUS_TODO = 1
    STATUS_IN_PROGRESS = 2
    STATUS_IN_PENDING = 3
    STATUS_DONE = 4
    STATUS_CHOICES = (
        (STATUS_TODO, ('A fazer')),
        (STATUS_IN_PROGRESS, ('Em Progresso')),
        (STATUS_IN_PENDING, ('Pendente')),
        (STATUS_DONE, ('Feito')),
    )
    id= models.AutoField(primary_key=True, db_column='id_task' )
    name = models.CharField(max_length=300, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    started = models.DateField(blank=True, null=True,)
    due = models.DateField(blank=True, null=True)
    completed = models.DateField(blank=True, null=True)
    sprint = models.ForeignKey(Sprint,  db_column='id_sprint',related_name='tasks' ,blank=True, null=True)
    responsible = models.ForeignKey(ScrumUser,  db_column='id_scrumuser',related_name='tasks' ,blank=True, null=True)
    project = models.ForeignKey(Project,  db_column='id_project',related_name='tasks' ,blank=True, null=True)

    def __str__(self):
        return self.name
    @classmethod
    def status_dic(cls):
        dic_values = [ ]
        for tupla in cls.STATUS_CHOICES:
            dicti = {}
            dicti['id'] = tupla[0]
            dicti['dominio'] = tupla[1]
            dic_values.append(dicti)

        return dic_values

class Impediment(BusinessModel):
    contextclassname = 'impediments'
    name = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    created_date = models.DateField(default=datetime.now)
    resolution_date = models.DateField(blank=True)
    task = models.ForeignKey(Task,  db_column='id_task',related_name='impediments' ,blank=True, null=True)
    sprint = models.ForeignKey(Sprint,  db_column='id_sprint',related_name='impediments' ,blank=True, null=True)


