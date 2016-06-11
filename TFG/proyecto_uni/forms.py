# -*- coding: utf-8 -*-
from django import forms 
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML, Field, Submit
from crispy_forms.bootstrap import InlineCheckboxes, FormActions


UNIVERSIDAD_CHOICES = (
    ('udc', 'UDC'),
    ('usc', 'USC'),
    ('uvigo', 'UVigo'),
)
CATEGORIA_CHOICES = (
    ('arte', 'Arte y Humanidades'),
    ('ccss', 'Ciencias Sociales'),
    ('ingenieria', 'Ingeniería y Arquitectura'),
    ('salud', 'Ciencias de la salud'), 
    ('ciencias', 'Ciencias'),
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
	
	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
	    	self.helper = FormHelper()
	    	# self.helper.form_class='form-horizontal'
	    	self.helper.layout = Layout(Field('estudio', css_class='form-group form-control'), InlineCheckboxes('universidad'), InlineCheckboxes('area_de_conocimiento'), FormActions(Submit('submit', 'Buscar')))