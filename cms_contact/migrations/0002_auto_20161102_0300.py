# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-02 02:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(blank=True, max_length=120, verbose_name='Street and number'),
        ),
    ]
