# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods

from .forms import LoginForm, UserRegistrationForm

from .models import Titulaciones


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
	if uni != '': 
		result = Titulaciones.objects.raw('SELECT * FROM titulaciones tit INNER JOIN impartida_en imp ON tit.codigo_titulacion = imp.codigo_titulacion INNER JOIN centros cent ON imp.codigo_centro = cent.codigo_centro WHERE cent.universidad = %s ', [uni]);
		return render(request, 'proyecto_uni/showstudies.html', {'result':result})
	else: 
		return render(request, 'proyecto_uni/studies.html')
