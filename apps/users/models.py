# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from ..users_auth.models import User

SEX_CHOICE = (
	('male', _('Male')),
	('female', _('Female'))
)


class Staff(User):

	def __str__(self):
		return self.username

	def __unicode__(self):
		return u'{}'.format(self.username)

	class Meta:
		verbose_name = _('Staff account')
		verbose_name_plural = _('Staff accounts')
