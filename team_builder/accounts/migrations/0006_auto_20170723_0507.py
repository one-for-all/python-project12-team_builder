# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-23 05:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20170723_0119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='skills',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_profiles', to='accounts.Skill'),
        ),
    ]
