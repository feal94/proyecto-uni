# -*- coding: utf-8 -*-

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Asignaturas(models.Model):
    codigo_asignatura = models.CharField(primary_key=True, max_length=25)
    nombre_asignatura = models.CharField(max_length=250, blank=True, null=True)
    guia_docente = models.CharField(max_length=150, blank=True, null=True)
    curso = models.SmallIntegerField(blank=True, null=True)
    regimen = models.CharField(max_length=100, blank=True, null=True)
    cuatrimestre = models.CharField(max_length=50, blank=True, null=True)
    creditos = models.SmallIntegerField(blank=True, null=True)
    mencion = models.CharField(max_length=150, blank=True, null=True)
    codigo_titulacion = models.ForeignKey('Titulaciones', models.DO_NOTHING, db_column='codigo_titulacion', blank=True, null=True)

    def __unicode__(self): 
        return self.nombre_asignatura

    class Meta:
    	managed= False
        db_table = 'asignaturas'


class Centros(models.Model):
    nombre_centro = models.CharField(max_length=100, blank=True, null=True)
    universidad = models.CharField(max_length=3, blank=True, null=True)
    campus = models.CharField(max_length=50, blank=True, null=True)
    codigo_centro = models.IntegerField(primary_key=True)

    def __unicode__(self): 
        return self.nombre_centro

    class Meta:
    	managed= False
        db_table = 'centros'


class ImpartidaEn(models.Model):
    codigo_centro = models.ForeignKey(Centros, models.DO_NOTHING, db_column='codigo_centro')
    codigo_titulacion = models.ForeignKey('Titulaciones', models.DO_NOTHING, db_column='codigo_titulacion')
    
    def __unicode__(self): 
        return self.codigo_titulacion + ' centro ' + self.codigo_centro

    class Meta:
    	managed= False
        db_table = 'impartida_en'
        unique_together = ('codigo_centro', 'codigo_titulacion',)


class Titulaciones(models.Model):
    codigo_titulacion = models.IntegerField(primary_key=True)
    nombre_titulacion = models.CharField(max_length=100, blank=True, null=True)
    nota_corte = models.FloatField(blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    def __unicode__(self): 
        return self.nombre_titulacion

    class Meta:
    	managed= False
        db_table = 'titulaciones'

class Encuestas(models.Model):
    codigo_titulacion = models.ForeignKey('Titulaciones', models.DO_NOTHING, db_column='codigo_titulacion', blank=True, null=True)
    ano_encuestas = models.CharField(max_length=10)
    grao_satisfaccion = models.FloatField(blank=True, null=True)

    def __unicode__(self): 
        return 'Encuestas ' + self.codigo_titulacion.nombre_titulacion + ' ' +self.ano_encuestas

    class Meta:
    	managed= False
        db_table = 'encuestas'
        unique_together = (('codigo_titulacion', 'ano_encuestas'),)

class Tasas(models.Model):
    codigo_titulacion = models.ForeignKey('Titulaciones', models.DO_NOTHING, db_column='codigo_titulacion', blank=True, null=True)
    ano_tasas = models.CharField(max_length=10)
    exito = models.FloatField(blank=True, null=True)
    rendimiento = models.FloatField(blank=True, null=True)
    evaluacion = models.FloatField(blank=True, null=True)
    abandono = models.FloatField(blank=True, null=True)

    def __unicode__(self): 
        return 'Tasas ' + self.codigo_titulacion.nombre_titulacion + ' ' +self.ano_tasas

    class Meta:
    	managed= False
        db_table = 'tasas'
        unique_together = (('codigo_titulacion', 'ano_tasas'),)
