# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 04:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('childrenrecipe', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='material',
            old_name='measureunits',
            new_name='portion',
        ),
        migrations.RemoveField(
            model_name='material',
            name='quantity',
        ),
    ]