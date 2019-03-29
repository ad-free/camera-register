# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..cameras.models import Camera
from ..commons.utils import token_key_generator

import uuid


class Token(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
	camera = models.ForeignKey(Camera, related_name='%(class)s_camera_publish_stream')
	token = models.CharField(_('Token'), max_length=150, unique=True)
	created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
	created_by = models.CharField(max_length=150, null=True)

	class Meta:
		verbose_name = _('Camera Token')
		unique_together = ('camera', 'token',)

	def save(self, *args, **kwargs):
		if not self.token:
			data = token_key_generator(serial=self.camera.serial, length=settings.TOKEN_SECRET_KEY_MAX_LENGTH, circle=settings.TOKEN_SECRET_KEY_CIRCLE)
			self.token = data['token']
		super(Token, self).save(*args, **kwargs)

	def __str__(self):
		return self.token

	def __unicode__(self):
		return u'{}'.format(self.token)


class EmbeddedCameraToken(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
	key = models.CharField(max_length=40, unique=True)
	camera = models.ForeignKey(Camera, related_name='%(class)s_camera')
	created_at = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		if not self.key:
			self.key = self.generate_key()
		return super(EmbeddedCameraToken, self).save(*args, **kwargs)

	def generate_key(self):
		return binascii.hexlify(os.urandom(20)).decode()
	generate_key.allow_tags = True

	def __str__(self):
		return self.key
