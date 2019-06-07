# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from ..commons.utils import encrypt_password
from ..cameras.models import Camera

import uuid

USER = 0
ADMIN = 1
MODIFIER = 2

TYPE = (
	(0, _('User')),
	(1, _('Admin')),
	(2, _('Modifier')),
)


class Account(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
	camera = models.ForeignKey(Camera, related_name='account_camera')
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=128, default=None, blank=True, null=True)
	old_password = models.CharField(max_length=128, default=None, blank=True, null=True)
	type = models.SmallIntegerField(choices=TYPE, default=ADMIN)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	created_by = models.CharField(max_length=150, null=True)

	class Meta:
		unique_together = (('camera', 'username',),)

	def __str__(self):
		return self.username

	def __unicode__(self):
		return u'{}'.format(self.username)

	def save(self, *args, **kwargs):
		if not self.password:
			self.password = encrypt_password(message='', secret=settings.CAMERA_ACCOUNT_SECRET_KEY)
		else:
			self.password = encrypt_password(message=self.password, secret=settings.CAMERA_ACCOUNT_SECRET_KEY)
		super(Account, self).save(*args, **kwargs)
