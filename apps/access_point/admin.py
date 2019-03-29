# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from ..access_point.models import AccessPoint


@admin.register(AccessPoint)
class AccessPointAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {'fields': ('name',)}),
	)
	list_display = ('name', 'created_by', 'created_at', 'modified_at',)
	ordering = ('name',)
	search_fields = ('name',)
	date_hierarchy = 'created_at'
	readonly_fields = ('password',)
