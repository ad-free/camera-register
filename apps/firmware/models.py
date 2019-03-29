# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..brand.models import Brand, DeviceType

import uuid


class Firmware(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
	name = models.CharField(max_length=50, blank=True, null=True)
	version = models.CharField(blank=True, null=True, max_length=150)
	release_file = models.FileField(blank=True, null=True, upload_to='firmware/%Y/%m/%d/')
	brand = models.ForeignKey(Brand, related_name='%(class)s_brand')
	type = models.ForeignKey(DeviceType, related_name='%(class)s_type')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
	modified_at = models.DateTimeField(auto_now=True)
	created_by = models.CharField(max_length=150, null=True)

	def __str__(self):
		return self.version

	def __unicode__(self):
		return u'{}'.format(self.version)
