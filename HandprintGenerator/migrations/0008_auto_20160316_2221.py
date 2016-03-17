# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-17 02:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HandprintGenerator', '0007_user_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionitemcomment',
            name='name',
        ),
        migrations.RemoveField(
            model_name='actionitemtag',
            name='user',
        ),
        migrations.RemoveField(
            model_name='actionitemvote',
            name='name',
        ),
        migrations.AddField(
            model_name='actionitemcomment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='HandprintGenerator.User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='actionitemtag',
            name='name',
            field=models.CharField(default='Water', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='actionitemvote',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='HandprintGenerator.User'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='actioniteminactive',
            name='reason',
            field=models.CharField(choices=[('duplicate', 'Duplicate'), ('other', 'Other'), ('spam', 'Spam')], max_length=15),
        ),
    ]
