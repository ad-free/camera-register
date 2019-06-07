# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe

from ..jsonform.settings import configs

from collections import OrderedDict

import json

configs.update(getattr(settings, 'JSON_SCHEMA_FORM', {}))


class JSONSchemaWidget(Widget):
	template_name = 'jsonform/json_widget.html'

	def __init__(self, sch, attrs=None):
		attrs = attrs or {}
		self.schema = sch
		super(JSONSchemaWidget, self).__init__(attrs)

	def get_context(self, name, value, attrs=None):
		opt = configs.get('options')

		opt.update({'startval': json.loads(value)})
		return {
			'id': attrs.get('id'),
			'name': name,
			'context': json.dumps({
				'id': attrs.get('id'),
				'attrs': attrs,
				'schema': self.schema,
				'options': opt
			}, sort_keys=True)
		}

	def render(self, name, value, attrs=None, renderer=None):
		context = self.get_context(name, value, attrs)
		template = loader.get_template(self.template_name).render(context)
		return mark_safe(template)

	class Media(object):
		static_url = getattr(settings, 'STATIC_URL')
		js = [
			static_url + 'assets/js/jsonschema-form.min.js',
			static_url + 'assets/js/jsoneditor.min.js'
		]
		css = {
			'all': {
				static_url + 'assets/css/bootstrap.min.css',
				static_url + 'assets/css/admin/styles.min.css'
			}
		}
