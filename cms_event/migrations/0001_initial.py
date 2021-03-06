# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-25 00:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.CharField(choices=[('YES', 'Yes'), ('NO', 'No'), ('MAYBE', 'Maybe')], max_length=12, verbose_name='You will go?')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=60, verbose_name='Name')),
                ('edition', models.PositiveSmallIntegerField(default=1, verbose_name='Edition')),
                ('slug', models.SlugField()),
                ('target', models.CharField(choices=[('LOCAL', 'Local'), ('REGION', 'Region'), ('COUNTRY', 'Country'), ('INTERNATIONAL', 'International')], default='LOCAL', max_length=18)),
                ('poster', models.ImageField(blank=True, null=True, upload_to='posters', verbose_name='Poster')),
                ('description', models.TextField(blank=True)),
                ('start_datetime', models.DateTimeField(blank=True, null=True, verbose_name='Start datetime')),
                ('end_datetime', models.DateTimeField(blank=True, null=True, verbose_name='End datetime')),
                ('booking', models.CharField(choices=[('OPTIONAL', 'Available'), ('REQUIRED', 'Required'), ('UNAVAILABLE', 'Free entry')], default='OPTIONAL', max_length=18)),
                ('total_seats', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Total seats')),
                ('website_url', models.URLField(blank=True, null=True, verbose_name='Website url')),
                ('booking_url', models.URLField(blank=True, null=True, verbose_name='Booking url')),
                ('schedule_url', models.URLField(blank=True, null=True, verbose_name='Schedule url')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PriceEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Price')),
                ('description', models.CharField(blank=True, max_length=150, verbose_name='Description')),
                ('seats', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Seats')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('custom_speakers', models.CharField(blank=True, max_length=150, verbose_name='Speakers who are not in the db')),
                ('start_datetime', models.DateTimeField(blank=True, null=True, verbose_name='Start datetime')),
                ('duration', models.DurationField(blank=True, null=True, verbose_name='Duration')),
                ('location', models.CharField(blank=True, help_text='Location within the building or buildings.', max_length=80, verbose_name='Location')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_event.Event')),
                ('interests', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Interests')),
            ],
        ),
    ]
