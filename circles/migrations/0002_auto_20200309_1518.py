# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-09 15:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='circle',
            old_name='verfied',
            new_name='verified',
        ),
    ]
