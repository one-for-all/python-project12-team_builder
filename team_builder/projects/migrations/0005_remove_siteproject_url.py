# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-23 06:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20170722_0434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteproject',
            name='url',
        ),
    ]
