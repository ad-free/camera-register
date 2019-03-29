# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Firmware


@admin.register(Firmware)
class FirmwareAdmin(admin.ModelAdmin):
	fields = ('version', 'release_file', 'brand', 'type',)
	list_display = ('version', 'brand', 'type', 'created_at', 'updated_at',)
	search_fields = ('version', 'created_at',)
	ordering = ['-created_at']

	def has_add_permission(self, request):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False
