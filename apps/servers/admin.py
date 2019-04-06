# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _

from models import Server


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
	fields = ('domain_name', 'ip_address', 'port', 'type', 'quantity', 'city', 'camera', 'ssl',)
	list_display = ('domain_name', 'ip_address', 'port', 'ssl', 'type', 'quantity', 'camera_quantity', 'city', 'created_at', 'modified_at',)
	search_fields = ('domain_name', 'ip_address', 'type', 'city', 'camera',)
	filter_horizontal = ('camera',)

	def save_model(self, request, obj, form, change):
		if request.user.is_superuser:
			if change:
				if int(obj.quantity) > obj.camera.count():
					obj.save()
				else:
					messages.set_level(request, messages.ERROR)
					messages.error(request, _('The amount of input must be greater than the quantity available.'))
					return False
			return super(ServerAdmin, self).save_model(request, obj, form, change)
		return False

	def camera_quantity(self, obj):
		return obj.camera.count()

	camera_quantity.short_description = _('Camera')
	camera_quantity.allow_tags = True
