# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_mysql.models import JSONField, Model
from ..cameras.models import Camera

import uuid

CONFIG_STATUS = (
	(0, _(u'Default')),
	(1, _(u'Modified')),
)


class Config(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
	name = models.CharField(max_length=50, unique=True)
	template = JSONField()
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	modified_at = models.DateTimeField(auto_now=True)
	created_by = models.CharField(max_length=150, null=True)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return u'{}'.format(self.name)


class ConfigCamera(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
	camera = models.ForeignKey(Camera, related_name="camera_config")
	name = models.CharField(max_length=50, blank=True)
	template = JSONField()
	status = models.PositiveIntegerField(choices=CONFIG_STATUS, default=0, verbose_name=_('Status'))
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	modified_at = models.DateTimeField(auto_now=True)
	created_by = models.CharField(max_length=150, null=True)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return u'{}'.format(self.name)
