# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address, validate_ipv6_address, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..cameras.models import Camera
from ..location.models import City

import uuid

TYPES = (
	(0, _(u'Live')),
	(1, _(u'Storage')),
	(2, _(u'Alert')),
	(3, _(u'MQTT')),
	(4, _(u'Wowza')),
	(5, _(u'SRS')),
)

STATUS = (
	(0, _(u'Offline')),
	(1, _(u'Online')),
)


def validate_ipv46_address(value):
	try:
		validate_ipv4_address(value)
	except ValidationError:
		try:
			validate_ipv6_address(value)
		except ValidationError:
			raise ValidationError(_('Enter a valid IPv4 or IPv6 address.'), code='invalid')


class Server(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
	ip_address = models.CharField(max_length=15, verbose_name=_('IP Address'), validators=[validate_ipv46_address])
	name = models.CharField(max_length=50, blank=True)
	domain_name = models.CharField(max_length=150, verbose_name=_('Host'))
	port = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(65535)])
	ssl = models.BooleanField(default=False)
	type = models.PositiveSmallIntegerField(choices=TYPES)
	quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)
	created_by = models.CharField(max_length=150, null=True)
	status = models.PositiveSmallIntegerField(choices=STATUS, default=0)
	city = models.ForeignKey(City, related_name='server_city')
	camera = models.ManyToManyField(Camera, blank=True, related_name='%(class)s_camera')

	class Meta:
		unique_together = (('ip_address', 'port', 'city',),)
		verbose_name_plural = _('Servers')

	def __str__(self):
		return '{ip_address}'.format(ip_address=self.ip_address)

	def __unicode__(self):
		return u'{ip_address}'.format(ip_address=self.ip_address)
