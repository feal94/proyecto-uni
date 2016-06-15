# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-12 17:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto_uni', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_usuario', models.CharField(max_length=80)),
                ('body', models.TextField()),
                ('titulacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='proyecto_uni.Titulaciones')),
            ],
        ),
    ]