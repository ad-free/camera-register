# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib import admin

from ..apis.apis import api_ftp_account_create
from .models import FTP


@admin.register(FTP)
class FTPAdmin(admin.ModelAdmin):
	fields = ('host', 'port', 'username', 'password', 'ssl', 'camera', 'server',)
	list_display = ('host', 'port', 'camera', 'server', 'ssl',)
	search_fields = ('ssl', 'host', 'camera', 'server',)
	ordering = ('username', 'host')

	def has_add_permission(self, request):
		if request.user.is_superuser:
			return True
		return False

	def has_delete_permission(self, request, obj=None):
		if request.user.is_superuser:
			return True
		return False

	def has_change_permission(self, request, obj=None):
		if request.user.is_superuser:
			return True
		return False

	def save_model(self, request, obj, form, change):
		if request.user.is_superuser:
			if not change:
				ftp_password = uuid.uuid4().hex
				api_ftp_account_create(username=obj.serial, password=ftp_password)
			return super(FTPAdmin, self).save_model(request, obj, form, change)
		return False
