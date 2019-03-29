# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

import uuid


class AccessPoint(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
	name = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Created At'))
	modified_at = models.DateTimeField(auto_now=True, verbose_name=_('Modified At'))
	created_by = models.CharField(max_length=150, null=True, verbose_name=_('Created By'))

	class Meta:
		unique_together = (('name', 'password'),)
		verbose_name = _('Access Point')
		verbose_name_plural = _('Access Points')

	def save(self, *args, **kwargs):
		if not self.name:
			self.password = settings.ACCESS_POINT_PASSWORD
		return super(AccessPoint, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return u'{}'.format(self.name)
