# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-23 18:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scrumuser',
            old_name='username',
            new_name='user_name',
        ),
    ]
