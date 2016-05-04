# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asignaturas',
            fields=[
                ('codigo_asignatura', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('guia_docente', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'db_table': 'asignaturas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Centros',
            fields=[
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('universidad', models.CharField(blank=True, max_length=3, null=True)),
                ('campus', models.CharField(blank=True, max_length=50, null=True)),
                ('codigo_centro', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'centros',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Encuestas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano_encuestas', models.CharField(max_length=10)),
                ('grao_satisfaccion', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'encuestas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ImpartidaEn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'impartida_en',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tasas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano_tasas', models.CharField(max_length=10)),
                ('exito', models.FloatField(blank=True, null=True)),
                ('rendimiento', models.FloatField(blank=True, null=True)),
                ('evaluacion', models.FloatField(blank=True, null=True)),
                ('abandono', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tasas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Titulaciones',
            fields=[
                ('codigo_titulacion', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('nota_corte', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'titulaciones',
                'managed': False,
            },
        ),
    ]