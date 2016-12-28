# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-26 10:06
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites_and_links', '0004_auto_20161226_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='domain',
            field=models.CharField(max_length=250, validators=[django.core.validators.RegexValidator(code='invalid_address', message='Domain cannot have www nad http/https', regex='^(?!www.|http:\\/\\/|https\\/\\/)$')]),
        ),
    ]
