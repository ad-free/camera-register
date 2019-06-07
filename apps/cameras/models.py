# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django_mysql.models import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from ..access_point.models import AccessPoint
from ..brand.models import Brand, DeviceType

import uuid

STATUS_DETAIL = (
	(0, _(u'Not used')),
	(1, _(u'Used')),
	(2, _(u'Deleted')),
)

STATUS = (
	(-1, _(u'Unknown')),
	(0, _(u'Online')),
	(1, _(u'Offline')),
)


class Camera(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
	name = models.CharField(max_length=100, blank=True, null=True, default=_('IPC Camera'))
	serial = models.CharField(max_length=30, unique=True)
	product_code = models.CharField(max_length=50, unique=True)
	status = models.IntegerField(choices=STATUS, default=-1, verbose_name=_('Status'))
	status_detail = models.PositiveSmallIntegerField(choices=STATUS_DETAIL, default=0, verbose_name=_('Detail'))
	is_publish = models.BooleanField(default=False, verbose_name=_('publish'))
	is_wza = models.BooleanField(default=False, verbose_name=_('wza'))
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True)
	modified_at = models.DateTimeField(auto_now=True)
	created_by = models.CharField(max_length=150, null=True)
	is_wifi = models.BooleanField(default=False, verbose_name=_('Wifi'))
	firmware = models.CharField(max_length=150)
	device_type = models.ForeignKey(DeviceType, blank=True, null=True, related_name='%(class)s_device_type')
	brand = models.ForeignKey(Brand, blank=True, null=True, related_name='%(class)s_brand')
	access_point = models.ForeignKey(AccessPoint, blank=True, null=True, related_name='%(class)s_access_point')

	class Meta:
		verbose_name = _('Camera')
		verbose_name_plural = _('Cameras')

	def save(self, *args, **kwargs):
		if not self.product_code:
			self.product_code = 'FCAM_{code}0000'.format(code=self.serial)
		super(Camera, self).save(*args, **kwargs)

	def __str__(self):
		return self.serial

	def __unicode__(self):
		return u'{}'.format(self.serial)


class CameraTopic(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
	camera = models.OneToOneField(Camera, related_name='camera_topic')
	topics = JSONField(blank=True, null=True)
	host = models.CharField(max_length=100, blank=True, null=True)
	port = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(65535)])
	ca_path = models.FileField(blank=True, null=True, upload_to=settings.API_QUEUE_CA_PATH, verbose_name=_('certificate'))
	ssl = models.BooleanField(default=False)

	def __str__(self):
		return '{}:{}'.format(self.host, self.port)

	def __unicode__(self):
		return u'{}:{}'.format(self.host, self.port)
