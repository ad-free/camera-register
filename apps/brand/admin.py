# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin

from models import Brand, DeviceType


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
	actions = ['delete_selected']
	fieldsets = (
		(None, {'fields': ('name', 'code_number',)}),
	)
	list_display = ('name', 'code_number', 'created_by', 'created_at', 'modified_at',)
	search_fields = ('name', 'code_number',)
	ordering = ('name',)
	# date_hierarchy = 'created_at'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
	actions = ['delete_selected']
	fieldsets = (
		(None, {'fields': ('name', 'image', 'devices_type',)}),
	)
	list_display = ('name', 'created_by', 'created_at', 'modified_at',)
	filter_horizontal = ('devices_type',)
	search_fields = ('name',)
	ordering = ('name',)
