# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('quantity', models.IntegerField()),
                ('measureunits', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seq', models.IntegerField()),
                ('describe', models.TextField()),
                ('image', models.ImageField(upload_to='images/exhibited_picture/%Y/%m/%d')),
                ('create_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('user', models.CharField(max_length=40, blank=True)),
                ('exihibitpic', models.ImageField(upload_to='exhibited_picture/%Y/%m/%d')),
                ('introduce', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='images/exhibited_picture/%Y/%m/%d')),
                ('pubdate', models.DateTimeField()),
                ('recipe', models.ForeignKey(to='childrenrecipe.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(to='childrenrecipe.Category')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(to='childrenrecipe.Tag'),
        ),
        migrations.AddField(
            model_name='procedure',
            name='recipe',
            field=models.ForeignKey(to='childrenrecipe.Recipe'),
        ),
        migrations.AddField(
            model_name='material',
            name='recipe',
            field=models.ForeignKey(to='childrenrecipe.Recipe'),
        ),
    ]
