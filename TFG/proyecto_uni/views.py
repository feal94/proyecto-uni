# -*- coding: utf-8 -*-

# Copyright 2016 Alvaro Feal 
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
# from django.contrib import admin


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist


from .forms import LoginForm, UserRegistrationForm, SearchForm, CommentForm, CompareTitulacionForm

from .models import Titulaciones, Tasas, Encuestas, Asignaturas, Comment

from .info import get_general_info, get_search_info, get_rest_info, get_compare_info

@require_http_methods(["GET"])
def index(request):
	return render (request, 'proyecto_uni/index.html')

def user_login(request):
	if request.method == 'GET': 
		form = LoginForm()
		return render (request, 'proyecto_uni/login.html', {'form':form})
	if request.method == 'POST': 
		form = LoginForm(request.POST)

		if form.is_valid(): 
			cd = form.cleaned_data
			user = authenticate(username=cd['username'], password=cd['password'])
			
			if user is not None: 
				login(request,user)
				messages.add_message(request, messages.SUCCESS, 'Has iniciado sesión con éxito!')
				return HttpResponseRedirect('/proyecto_uni/')
			else:
				messages.error(request, "Usuario o contraseña incorrectos")
				return render(request, 'proyecto_uni/login.html', {'form':LoginForm})
		else: 
			messages.error(request, "Usuario o contraseña incorrectos")
			return render(request, 'proyecto_uni/login.html', {'form':LoginForm})
	else: 
		return HttpResponse("I'm lost")

@login_required
@require_http_methods(["GET"])
def user_logout(request): 
	logout(request)
	messages.add_message(request, messages.SUCCESS, 'Has cerrado sesión con éxito!')
	return HttpResponseRedirect('/proyecto_uni/')

def user_signup(request): 
	if request.method == 'POST': 
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid(): 
			new_user = user_form.save(commit=False)
			new_user.set_password(
				user_form.cleaned_data['password'])
			new_user.save()
			messages.add_message(request, messages.SUCCESS, 'Usuario creado con éxito!')
			return HttpResponseRedirect('/proyecto_uni/')
	else: 
		user_form = UserRegistrationForm()
	return render(request,'proyecto_uni/signup.html', {'user_form':user_form})

@require_http_methods(["GET"])
def about(request):
	return render(request, 'proyecto_uni/about.html')

@require_http_methods(["GET"])
def contact(request):
	return render(request, 'proyecto_uni/contact.html')

@require_http_methods(["GET"])
def studies(request):
	uni = request.GET.get('uni', '')
	if uni == '': 
		return render(request, 'proyecto_uni/studies.html')
	elif uni == 'SUG':
		result = get_search_info(['udc','usc','uvigo'], None, None, None, None, None, None)
	else:
		result = get_search_info([uni], None, None, None, None, None, None)
	rest = get_rest_info(result, True)
	rest = rest[0].order_by('impartidaen__codigo_titulacion__nombre_titulacion')
	result = result.order_by('nombre_titulacion')

	result = zip(result, rest)
	if len(result) == 0:
		messages.error(request,"No se han encontrado resultados para estos parámetros de búsqueda")
		return HttpResponseRedirect('/proyecto_uni/studies')
	return render(request, 'proyecto_uni/showstudies.html', {'result':result})

@require_http_methods(["GET"])
def details(request):
	estudio = request.GET.get('estudio', '')
	uni = request.GET.get('uni', '')
	campus = request.GET.get('campus', '')
	rate = None
	info_general = get_general_info(uni, estudio, campus)
	rest = get_rest_info(info_general, False)
	comments = Comment.objects.filter(codigo_titulacion=info_general[0].codigo_titulacion)
	mencion = False
	if rest[1] is not None:
		for foo in rest[1]: 
			if foo.mencion != 'null':
				mencion = True
				break
	rate = Titulaciones.objects.get(pk=info_general.values('codigo_titulacion'))
	return render(request, 'proyecto_uni/details.html', {'info_general':info_general[0], 'info_universidad':rest[0], 'rate':rate, 'info_resultados_academicos':rest[2], 'info_resultados_encuestas': rest[3], 'info_asignaturas': rest[1], 'comments':comments, 'mencion':mencion})


def search(request): 
	if request.method == 'POST': 
		search_form = SearchForm(request.POST)
		if search_form.is_valid():
			cd = search_form.cleaned_data
			result = get_search_info(cd['universidad'], cd['estudio'], cd['area_de_conocimiento'], cd['accion'], cd['nota_de_corte'], cd['accion2'], cd['tasa_de_abandono'])	
			if (result is not None) and (len(result) > 0):
				rest = get_rest_info(result, True)
				result = zip(result, rest[0])
				return render(request, 'proyecto_uni/showstudies.html', {'result':result})
			else:
				messages.warning(request, "No hemos encontrado resultados para esos parámetros de búsqueda")
				return HttpResponseRedirect("/proyecto_uni/search")	
		else:
			messages.error(request, "Los parámetros de búsqueda son insuficientes o incorrectos ")
			return HttpResponseRedirect("/proyecto_uni/search")
	else: 
		search_form = SearchForm
		return render(request,'proyecto_uni/advanced_search.html', {'search_form': search_form})

@login_required
def comment(request): 
	if request.method == 'POST': 
		comments = Comment.objects
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid(): 
			cd = comment_form.cleaned_data
			old_comment = comments.filter(nombre_usuario=request.user.username).filter(codigo_titulacion=cd['codigo_titulacion'])
			if (old_comment is None) or (len(old_comment) == 0):
				new_comment = comment_form.save(commit=False)
				new_comment.nombre_usuario = request.user.username
				new_comment.save()
				messages.success(request, "Comentario añadido con éxito")
				return HttpResponseRedirect('/proyecto_uni')
			else:
				messages.warning(request, "Solo se puede poner un comentario para cada estudio, puedes editar tu comentario")
				return HttpResponseRedirect('/proyecto_uni/comment/edit?pk='+str(cd['codigo_titulacion'].codigo_titulacion))
		else: 
			messages.error(request, "Ha habido un error a la hora de guardar tu comentario")
			return render(request, 'proyecto_uni/post_comment', {'comment_form':comment_form})
	else: 
		pk = request.GET.get('pk','')
		old_comment = Comment.objects.filter(nombre_usuario=request.user.username).filter(codigo_titulacion=pk)
		if (old_comment is None) or (len(old_comment) == 0):
			comment_form = CommentForm(initial={'codigo_titulacion':pk})
			return render(request, 'proyecto_uni/post_comment.html',{'comment_form':comment_form})
		else: 
			messages.warning(request, "Solo se puede poner un comentario para cada estudio, puedes editar tu comentario")
			return HttpResponseRedirect('/proyecto_uni/comment/edit?pk='+pk)

@login_required
def edit_comment(request):
	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid(): 
			cd = comment_form.cleaned_data
			old_comment = Comment.objects.filter(nombre_usuario=request.user.username).filter(codigo_titulacion=cd['codigo_titulacion'])
			if (old_comment is not None) and (len(old_comment) > 0): 
				old_comment.update(comentario=cd['comentario'])
				messages.success(request,"Comentario modificado con éxito")
				return HttpResponseRedirect('/proyecto_uni')
			else: 
				messages.error(request, "Ha habido un error a la hora de guardar tu comentario")
				return render(request, 'proyecto_uni/edit_comment', {'comment_form':comment_form})
		else: 
			messages.error(request, "Ha habido un error a la hora de guardar tu comentario")
			return render(request, 'proyecto_uni/edit_comment', {'comment_form':comment_form})
	else: 
		pk = request.GET.get('pk','')
		old_comment = Comment.objects.filter(nombre_usuario=request.user.username).filter(codigo_titulacion=pk)
		comment_form = CommentForm(initial={'codigo_titulacion':pk, 'comentario':old_comment[0].comentario})
		return render(request, 'proyecto_uni/edit_comment.html',{'comment_form':comment_form})

@login_required
def delete_comment(request):
	pk = request.GET.get('pk','')
	return render(request, 'proyecto_uni/confirm_delete.html', {'pk':pk})

@login_required
def delete_confirm(request):
	pk = request.GET.get('pk','')
	old_comment = Comment.objects.filter(nombre_usuario=request.user.username).filter(codigo_titulacion=pk)
	if (old_comment is not None) and (len(old_comment) > 0): 
		old_comment.delete()
		messages.success(request, "El comentario ha sido borrado con éxito")
		return HttpResponseRedirect('/proyecto_uni')
	else:
		messages.error(request,"Ha habido un error en el proceso de borrado del comentario")
		return HttpResponseRedirect('/proyecto_uni')

def choose_campus(request): 
	if request.method == 'POST':
		empty = '----------'
		campus1 = request.POST.get('campus1')
		campus2 = request.POST.get('campus2')
		campus3 = request.POST.get('campus3')
		if (campus1 != empty) or (campus2 != empty) or (campus3 != empty):
				if campus1 != empty:
					titulacion1_form=CompareTitulacionForm(campus1, prefix="estudio1")
				else: 
					titulacion1_form = None
				if campus2 != empty: 
					titulacion2_form = CompareTitulacionForm(campus2, prefix="estudio2")
				else: 
					titulacion2_form = None
				if campus3 != empty:
					titulacion3_form = CompareTitulacionForm(campus3, prefix="estudio3")
				else: 
					titulacion3_form = None
				
				return render(request,'proyecto_uni/choose_estudio.html', {"tit1":titulacion1_form, "tit2":titulacion2_form, "tit3":titulacion3_form})
		else: 
			messages.error(request,"Ha habido un error con los datos proporcionados")
			return HttpResponseRedirect('/proyecto_uni/compare')
		
	else: 
		return render(request, 'proyecto_uni/choose_campus.html')

def choose_titulacion(request):
	if request.method == 'POST': 
		tit1 = request.POST.get('estudio1-nombre_titulacion')
		tit2 = request.POST.get("estudio2-nombre_titulacion")
		tit3 = request.POST.get("estudio3-nombre_titulacion")
		if (tit1 is not None and tit1 != '') or (tit2 is not None and tit2 != '') or (tit3 is not None and tit3 != ''):
			if tit1 is not None: 
				info1 = get_compare_info(tit1)
			else: 
				info1 = None
			if tit2 is not None: 
				info2 = get_compare_info(tit2)
			else:
				info2 = None
			if tit3 is not None: 
				info3 = get_compare_info(tit3)
			else: 
				info3 = None
			return render(request, 'proyecto_uni/compare.html', {'info1':info1, 'info2':info2, 'info3':info3})
		else: 
			messages.error(request,'Ha habido un error con los datos proporcionados')
			return HttpResponseRedirect('/proyecto_uni/compare')
