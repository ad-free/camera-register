# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Account


@admin.register(Account)
class CameraAccountAdmin(admin.ModelAdmin):
	fieldsets = (
		(_('Camera'), {'fields': ('camera',)}),
		(_('Account'), {'fields': ('username', 'password', 'type',)}),
	)
	list_display = ('camera', 'username', 'type', 'created_by', 'created_at')
	search_fields = ('username',)
	readonly_fields = ('old_password',)

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_by = str(request.user)
			obj.save()
		return super(CameraAccountAdmin, self).save_model(request, obj, form, change)
