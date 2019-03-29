# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import EmbeddedCameraToken


@admin.register(EmbeddedCameraToken)
class EmbeddedCameraTokenAdmin(admin.ModelAdmin):
	fields = ('camera', 'key',)
	list_display = ('camera', 'key', 'created_at',)
	readonly_fields = ('created_at', 'key', 'camera',)
	search_fields = ('camera', 'key',)

	def has_delete_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request):
		return False
