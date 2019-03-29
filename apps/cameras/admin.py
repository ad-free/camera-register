# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Camera

import logging

logger = logging.getLogger('')


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
	fields = ('serial', 'device_type', 'brand', 'access_point', 'status_detail', 'is_wifi')
	list_display = (
		'serial', 'brand', 'device_type', 'firmware',
		'created_at', 'updated_at', 'created_by', 'status_detail', 'status', 'is_publish', 'is_wza', 'is_wifi',
	)
	search_fields = ('name', 'serial', 'product_code', 'status_detail', 'is_wifi', 'status', 'server')
	ordering = ('serial', 'status',)
	readonly_fields = ('is_wza', 'firmware')
	# date_hierarchy = 'created_at'
