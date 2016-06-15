# -*- coding: utf-8 -*-
from django import forms 
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML, Field, Submit
from crispy_forms.bootstrap import InlineCheckboxes, FormActions, StrictButton

from .models import Comment, Titulaciones, Centros


UNIVERSIDAD_CHOICES = (
    ('udc', 'UDC'),
    ('usc', 'USC'),
    ('uvigo', 'UVigo'),
)
CATEGORIA_CHOICES = (
    ('Arte y Humanidades', 'Arte y Humanidades'),
    ('Ciencias Sociales y Jurídicas', 'Ciencias Sociales'),
    ('Ingeniería y Arquitectura', 'Ingeniería y Arquitectura'),
    ('Ciencias de la Salud', 'Ciencias de la salud'), 
    ('Ciencias', 'Ciencias'),
)
ACCION_CHOICES = (
    ('>=', '>='),
    ('<=', '<='),
    ('=', '='),
)


class LoginForm(forms.Form): 
	username = forms.CharField(label='Usuario')
	password = forms.CharField(label='Contraseña',widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm): 
	password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
	password_2 = forms.CharField(label='Repita la contraseña', widget=forms.PasswordInput)



	class Meta: 
		model = User
		fields = ('username','first_name','last_name','email',)
	
	def check_password(self): 
		cd = self.cleaned_data
		if cd['password'] != cd['password_2']: 
			raise forms.ValidationError('Las contraseñas no son iguales')
		return cd['password_2']

class SearchForm(forms.Form):
	universidad = forms.MultipleChoiceField(
		required=False, 
		widget = forms.CheckboxSelectMultiple,
		choices=UNIVERSIDAD_CHOICES,
		)
	estudio = forms.CharField(required=False, widget= forms.TextInput(attrs={'autocomplete':'off'}))

	area_de_conocimiento = forms.MultipleChoiceField(
		required=False,
		widget = forms.CheckboxSelectMultiple,
		choices=CATEGORIA_CHOICES,
		)

	accion= forms.ChoiceField(
		label = 'Acción',
		required=False, 
		choices= ACCION_CHOICES,
		)

	nota_de_corte = forms.FloatField(
		required=False, 
		max_value = 14.0, 
		min_value = 5.0,
		)

	accion2= forms.ChoiceField(
		label = 'Acción',
		required=False, 
		choices= ACCION_CHOICES,
		)

	tasa_de_abandono = forms.FloatField(
		required=False, 
		max_value= 100.0,
		min_value = 0.0,
		) 
	
	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
	    	self.helper = FormHelper()
	    	# self.helper.form_class='form-horizontal'
	    	self.helper.layout = Layout(Field('estudio', css_class='form-group form-control'), InlineCheckboxes('universidad'), InlineCheckboxes('area_de_conocimiento'), Fieldset('Escoge el operador que te interesa y el valor de la nota de corte','accion','nota_de_corte', css_class = 'form-group'), Fieldset('Escoge el operador que te interesa y el valor de la tasa de abandono', 'accion2', 'tasa_de_abandono', css_class= 'form-group'), FormActions(Submit('submit', 'Buscar')))

class CommentForm(forms.ModelForm):
	class Meta: 
		model = Comment
		fields = ('comentario','codigo_titulacion')
		widgets = {'codigo_titulacion': forms.HiddenInput()}

class CompareTitulacionForm(forms.ModelForm):
	titulacion = forms.ModelChoiceField(queryset=Titulaciones.objects)

	class Meta: 
		model = Titulaciones
		fields = ('titulacion',)

class CompareUniversidadForm(forms.ModelForm):
	campus = forms.ModelChoiceField(queryset=Centros.objects, to_field_name="campus")

	class Meta: 
		model = Centros
		fields = ('campus',)