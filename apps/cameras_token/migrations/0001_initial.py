# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-29 07:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cameras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmbeddedCameraToken',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=40, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='embeddedcameratoken_camera', to='cameras.Camera')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=150, unique=True, verbose_name='Token')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('created_by', models.CharField(max_length=150, null=True)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_camera_publish_stream', to='cameras.Camera')),
            ],
            options={
                'verbose_name': 'Camera Token',
            },
        ),
        migrations.AlterUniqueTogether(
            name='token',
            unique_together=set([('camera', 'token')]),
        ),
    ]