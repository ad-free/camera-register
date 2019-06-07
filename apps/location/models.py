# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..commons.utils import remove_special_chars

import uuid


class City(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
	name = models.CharField(max_length=150)
	lat = models.FloatField(blank=True, null=True)
	lon = models.FloatField(blank=True, null=True)
	order = models.PositiveIntegerField(default=1, verbose_name=_('Order number'))
	status = models.BooleanField(default=True)
	created_by = models.CharField(max_length=150, null=True)

	def save(self, *args, **kwargs):
		self.name = remove_special_chars(self.name)
		super(City, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = _('Cities')

	def __str__(self):
		return self.name

	def __unicode__(self):
		return u'{}'.format(self.name)
