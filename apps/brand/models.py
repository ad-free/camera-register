# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

import uuid


class DeviceType(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
	name = models.CharField(max_length=50, blank=True, null=True)
	code_number = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
	modified_at = models.DateTimeField(auto_now=True, verbose_name=_('Modified At'))
	created_by = models.CharField(max_length=150, null=True)

	class Meta:
		unique_together = ('code_number',)
		verbose_name = _('Device Type')
		verbose_name_plural = _('Devices Type')

	def __str__(self):
		return self.code_number

	def __unicode__(self):
		return u'{}'.format(self.code_number)


class Brand(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
	name = models.CharField(max_length=50)
	image = models.ImageField(upload_to=settings.PATH_IMAGE_BRAND, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=settings.IMAGE_FILE_FORMAT)])
	created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
	modified_at = models.DateTimeField(auto_now=True, verbose_name=_('Modified At'))
	devices_type = models.ManyToManyField(DeviceType, blank=True, related_name='%(class)s_devices_type')
	created_by = models.CharField(max_length=150, null=True)

	class Meta:
		unique_together = ('name',)
		verbose_name = _('Brand', )
		verbose_name_plural = _('Brands', )

	def __str__(self):
		return self.name

	def __unicode__(self):
		return u'{}'.format(self.name)
