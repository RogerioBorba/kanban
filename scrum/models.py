from __future__ import unicode_literals
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
from datetime import datetime
from django.db import models

# Create your models here.
from hyper_resource.models import BusinessModel

class ScrumUser(BusinessModel):
    contextclassname = 'user-list'
    name = models.CharField(max_length=100, blank=True, default='')
    user_name = models.CharField(max_length=100, unique=True )
    email = models.CharField(max_length=100, unique=True, null=True)
    password  = models.CharField(max_length=100, unique=True )
    description = models.TextField(blank=True, null=True, default='')
    role = models.CharField(max_length=100, blank=True, default='user')
    avatar = models.CharField(max_length=200, blank=True, default='')
    ativo = models.NullBooleanField()

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
    name = models.CharField(max_length=100 )
    description = models.TextField(blank=True, null=True, default='')
    start = models.DateField(null=True,blank=True)
    end = models.DateField(null=True, blank=True)
    real_end = models.DateField(null=True, blank=True)
    responsible = models.ForeignKey(ScrumUser,  db_column='id_scrumuser',related_name='sprints', blank=True, null=True)

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


