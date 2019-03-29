# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework.authtoken.models import Token


def user_detail(user):
	try:
		token = user.auth_token.key
	except:
		token = Token.objects.create(user=user)
		token = token.key
	user_json = {
		'id': user.pk,
		'token': token,
	}
	return user_json
