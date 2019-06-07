# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from ..cameras.models import Camera
from ..servers.models import Server

from ..commons.utils import encrypt_password

import uuid


class FTP(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
	host = models.CharField(max_length=100)
	port = models.PositiveIntegerField(default=21, validators=[MinValueValidator(0), MaxValueValidator(65535)])
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=150)
	ssl = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	is_online = models.BooleanField(default=False, verbose_name=_('Online'))
	camera = models.ForeignKey(Camera, related_name='%(class)s_camera')
	server = models.ForeignKey(Server, related_name='%(class)s_server')

	class Meta:
		unique_together = ('host', 'port', 'username', 'camera', 'server')

	def save(self, *args, **kwargs):
		if 'ftp://' in self.host:
			self.host = self.host.replace('ftp://', '')
		elif 'ftps://' in self.host:
			self.host = self.host.replace('ftps://', '')
		if self.ssl:
			self.host = 'ftps://{host}'.format(host=self.host)
		else:
			self.host = 'ftp://{host}'.format(host=self.host)
		if not self.password:
			self.password = encrypt_password(message=uuid.uuid1().hex, secret=settings.FTP_SECRET_KEY)
		else:
			self.password = encrypt_password(message=self.password, secret=settings.FTP_SECRET_KEY)
		return super(FTP, self).save(*args, **kwargs)

	def __str__(self):
		return '{host}:{port}[{username}]'.format(host=self.host, port=self.port, username=self.username)

	def __unicode__(self):
		return u'{host}:{port}[{username}]'.format(host=self.host, port=self.port, username=self.username)
