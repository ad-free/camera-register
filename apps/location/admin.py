# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
	fields = ('name', 'lat', 'lon', 'order', 'status',)
	list_display = ('name', 'lat', 'lon', 'order', 'status',)
	search_fields = ('name', 'order', 'status',)
	ordering = ('name', 'status',)
	
	def save_model(self, request, obj, form, change):
		if request.user.is_superuser:
			return super(CityAdmin, self).save_model(request, obj, form, change)
		return False
