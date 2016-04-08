# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-06 01:14
from __future__ import unicode_literals

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('HandprintGenerator', '0005_auto_20160405_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionideatag',
            name='action_idea',
        ),
        migrations.RemoveField(
            model_name='actionideatag',
            name='user',
        ),
        migrations.AddField(
            model_name='actionidea',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.DeleteModel(
            name='ActionIdeaTag',
        ),
    ]