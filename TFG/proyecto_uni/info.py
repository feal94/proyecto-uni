# -*- coding: utf-8 -*-
from .models import Titulaciones, ImpartidaEn, Centros, Asignaturas, Tasas, Encuestas
from django.db.models import Q

def get_general_info(uni, estudio, campus): 
	general_info = filter_by_campus(campus, None)
	return filter_by_estudio(estudio, general_info, True)

def get_rest_info(info_general, list): 
	#list is zero when there's only one titulacion
	info_universidad = get_universidad_info(info_general)
	if not list: 
		info_universidad = info_universidad[0]
	
	info_resultados_academicos = get_resultados_academicos_info(info_general)
	if len(info_resultados_academicos) == 0: 
		info_resultados_academicos = None
	else: 
		if not list: 
			info_resultados_academicos = info_resultados_academicos[0]

	info_resultados_encuestas = get_resultados_encuestas_info(info_general)
	if len(info_resultados_encuestas) == 0: 
		info_resultados_encuestas = None
	else: 
		if not list:
			info_resultados_encuestas = info_resultados_encuestas[0]

	info_asignaturas = get_asignaturas_info(info_general)
	if len(info_asignaturas) == 0: 
		info_asignaturas = None

	return[info_universidad, info_asignaturas, info_resultados_academicos, info_resultados_encuestas]

def get_universidad_info(titulaciones):
	titulaciones_list = titulaciones.values('codigo_titulacion')
	return Centros.objects.filter(impartidaen__codigo_titulacion__in=titulaciones_list)

def get_asignaturas_info(titulaciones):
	titulaciones_list = titulaciones.values('codigo_titulacion')
	return Asignaturas.objects.filter(codigo_titulacion__in=titulaciones_list).order_by('cuatrimestre')

def get_resultados_academicos_info(titulaciones): 
	titulaciones_list = titulaciones.values('codigo_titulacion')
	return Tasas.objects.filter(codigo_titulacion__in= titulaciones_list)

def get_resultados_encuestas_info(titulaciones): 
	titulaciones_list = titulaciones.values('codigo_titulacion')
	return Encuestas.objects.filter(codigo_titulacion__in= titulaciones_list)

def get_search_info(universidad, estudio, area, accion, nota, accion2, abandono):
	result = None
	if estudio:
		result =  filter_by_estudio(estudio, result, False)
		if result is None: #Si la búsqueda falla no seguimos
			return None
	if len(universidad) > 0:
		result = filter_by_universidad(universidad, result)
	if area and (len(area) > 0): 
		result = filter_by_area(area, result)
	if accion and nota: 
		result = filter_by_nota(accion, nota, result)	
	if accion2 and abandono:
		result = filter_by_abandono(accion2, abandono, result)	
	return result

def filter_by_universidad(universidad, qs): 
	if qs is not None: 
		titulaciones = qs
	else: 
		titulaciones = Titulaciones.objects

	if len(universidad) == 1: 
		return titulaciones.filter(impartidaen__codigo_centro__universidad=universidad[0])
	elif len(universidad) == 2: 
		return titulaciones.filter(Q(impartidaen__codigo_centro__universidad=universidad[0]) | Q(impartidaen__codigo_centro__universidad=universidad[1]))
	else: 
		return titulaciones

def filter_by_campus(campus, qs): 
	if qs is not None: 
		return qs.filter(impartidaen__codigo_centro__universidad__campus = campus)
	else: 
		return Titulaciones.objects.filter(impartidaen__codigo_centro__campus = campus)

def filter_by_estudio(estudio, qs, exact):
	if qs is not None: 
		titulaciones = qs
	else: 
		titulaciones = Titulaciones.objects 

	if exact: 
		return titulaciones.filter(nombre_titulacion=estudio)
	else:
		return titulaciones.filter(nombre_titulacion__icontains=estudio)

def filter_by_area(area, qs): 
	if qs is not None: 
		titulaciones = qs
	else: 
		titulaciones = Titulaciones.objects
	if len(area) == 1: 
		return titulaciones.filter(categoria__iexact=area[0])
	elif len(area) == 2:
		return titulaciones.filter(Q(categoria__iexact=area[0]) | Q(categoria__iexact=area[1])) 
	elif len(area) == 3: 
		return titulaciones.filter(Q(categoria__iexact=area[0]) | Q(categoria__iexact=area[1]) | Q(categoria__iexact=area[2]))
	elif len(area) == 4: 
		return titulaciones.filter(Q(categoria__iexact=area[0]) | Q(categoria__iexact=area[1]) | Q(categoria__iexact=area[2]) | Q(categoria__iexact=area[3]))
	else: 
		return titulaciones

def filter_by_nota(accion, nota, qs):  
	if qs is not None: 
		titulaciones = qs
	else: 
		titulaciones = Titulaciones.objects

	if accion == '>=': 
		return titulaciones.filter(nota_corte__gte=nota)
	if accion == '<=': 
		return titulaciones.filter(nota_corte__lte=nota)
	if accion == '=': 
		return titulaciones.filter(nota_corte=nota)

def filter_by_abandono(accion, abandono, qs):
	if qs is not None: 
		titulaciones = qs
	else: 
		titulaciones = Titulaciones.objects
	if accion == '>=': 
		return titulaciones.filter(tasas__abandono__gte=abandono)
	if accion == '<=': 
		return titulaciones.filter(tasas__abandono__lte=abandono)
	if accion == '=': 
		return titulaciones.filter(tasas__abandono=abandono)
