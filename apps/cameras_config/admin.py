# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from ..cameras.models import CameraTopic
from .models import Config, ConfigCamera

from ..commons.utils import publish_topic_mqtt
from ..jsonform.widgets import JSONSchemaWidget

import json


class CameraConfigForm(forms.ModelForm):
	class Meta:
		model = ConfigCamera
		fields = ('name', 'template', 'status', 'camera')
		widgets = {
			'template': JSONSchemaWidget(sch=settings.JSON_SCHEMA_FORM)
		}

	def __init__(self, *args, **kwargs):
		super(CameraConfigForm, self).__init__(*args, **kwargs)
		if not self.initial:
			self.fields['template'] = forms.ModelChoiceField(Config.objects.all())
			self.fields['name'].widget = forms.HiddenInput()


class ConfigDefaultForm(forms.ModelForm):
	class Meta:
		model = Config
		fields = '__all__'
		widgets = {
			'template': JSONSchemaWidget(sch=settings.JSON_SCHEMA_FORM)
		}


@admin.register(ConfigCamera)
class CameraConfigAdmin(admin.ModelAdmin):
	readonly_fields = ('status',)
	form = CameraConfigForm
	actions = ['submit_config_selected']
	list_display = ('camera', 'name', 'status', 'created_at', 'modified_at',)
	search_fields = ('name',)
	ordering = ('name',)

	def save_model(self, request, obj, form, change):
		if not change:
			obj.name = obj.template.name
			obj.template = obj.template.template
		else:
			if 'template' in form.changed_data or 'name' in form.changed_data:
				obj.status = 1
		obj.save()

	class Media(object):
		static_url = getattr(settings, 'STATIC_URL')
		js = [
			static_url + 'assets/js/jsconfig-camera.js',
		]

	def submit_config_selected(self, request, query):
		for obj in query:
			user = obj.camera.serial
			password = obj.camera.serial
			try:
				camera_topic = CameraTopic.objects.get(camera='1').topics
			except CameraTopic.DoesNotExist:
				messages.error(request, _('Can not find any topics for [{}] camera').format(obj.camera.serial))
			else:
				topic = camera_topic['publish'].get('addcfg')
				value = json.dumps(obj.template)
				publish_topic_mqtt(user, password, topic, value)
		return messages.info(request, _('Send config to cameras successfully'))

	def submit_config_for_camera(self, obj):
		return format_html(
			'<button type="button" class="submit-config" data-config="{}" data-serial="{}" data-url="{}">{}</button>', obj.template, obj.camera.serial, reverse('api_camera_config_submit'), _('Submit'),
		)

	submit_config_for_camera.allow_tags = True
	submit_config_for_camera.short_description = _('Change config')


@admin.register(Config)
class ConfigDefaultAdmin(admin.ModelAdmin):
	form = ConfigDefaultForm
	fields = ('name', 'template')
	list_display = ('name', 'created_at', 'modified_at',)
	ordering = ('name',)
