# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-23 14:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites_and_links', '0002_auto_20161222_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkScan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(default='/', max_length=300)),
                ('title', models.CharField(blank=True, default='', max_length=400, null=True)),
                ('description', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('h1', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('custom_code', models.TextField(blank=True, default='', max_length=3000, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites_and_links.Link')),
            ],
        ),
    ]
