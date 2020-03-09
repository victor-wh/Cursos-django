# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

class CRideModel(models.Model):
	created = models.DateTimeField('created at',auto_now_add=True,help_text='Fecha en que el objeto fue creado')
	modified = models.DateTimeField('modified at', auto_now=True, help_text='Fecha en que el objeto fue modificado')

	class Meta:
		abstract = True

		get_latest_by = 'created'
		ordering = ['-created', '-modified']

class User(CRideModel, AbstractUser):
	'''
	Extend from django's abstract user.
	'''
	email = models.EmailField('email_address',unique=True)
	phone_regex = RegexValidator(
		regex=r'\+?1?\d{9,15}$',
		message="Phone number debe ser de 10 numeros"
	)
	phone_number = models.CharField(validators=[phone_regex],max_length=17,blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name','last_name']

	is_client = models.BooleanField(
		'client status',
		default=True,
		help_text=(
			'Ayuda para usuarios'
		)
	)
	is_verified = models.BooleanField(
		'verified',
		default=True,
		help_text = 'Usuario verificado'
	)

	def __str__(self):
		return self.username
	
	def get_short_name(self):
		return self.username