# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework import status
from django.conf import settings

from .configs import *

import requests
import json
import os


class SignInTestCase(TestCase):
	def setUp(self):
		self.url = ''
		self.gis = API_MANAGEMENT_GIS
		self.content_type = 'application/json'

		if not API_MANAGEMENT_LOCAL:
			self.url = API_MANAGEMENT_LIST['sign-in'].format(
					protocol=API_MANAGEMENT_PROTOCOL,
					host=API_MANAGEMENT_HOST
			)
		else:
			self.url = API_MANAGEMENT_LIST_LOCAL['sign-in'].format(
					protocol=API_MANAGEMENT_PROTOCOL_LOCAL,
					host=API_MANAGEMENT_HOST_LOCAL,
					port=API_MANAGEMENT_PORT_LOCAL
			)

	def test_sign_in(self):
		with open(os.path.join(settings.BASE_DIR, 'apps/apis/test/test_cases/sign_in.json'), 'r') as f:
			cases = json.loads(f.read())
			for case in cases['data']:
				request = requests.post(url=self.url, data=json.dumps(case), headers={'gis': self.gis, 'content-type': 'application/json'})
				data = json.loads(request.content)
				if data['status'] == status.HTTP_200_OK:
					print('[+] %s' % case)
					print('[+] %s' % data['data'])
					print('[!] ----- Pass -----')
				else:
					print('[X] %s' % case)
					self.assertNotEqual(data['status'], status.HTTP_400_BAD_REQUEST, data['errors'])
