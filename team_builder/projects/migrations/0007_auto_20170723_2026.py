# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-23 20:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20170723_0714'),
    ]

    operations = [
        migrations.RenameField(
            model_name='position',
            old_name='user',
            new_name='applicant',
        ),
        migrations.AlterField(
            model_name='siteproject',
            name='applicant_requirements',
            field=models.TextField(blank=True),
        ),
    ]
