# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from ..commons.utils import logger_format

import json
import requests
import logging

logger = logging.getLogger('')


def api_ftp_account_create(username, password):
	url = '{protocol}://{host}/account/create'.format(
			protocol=settings.API_FTP_PROTOCOL,
			host=settings.API_FTP_HOST
	)
	
	data = {
		'username': username,
		'password': password
	}
	
	try:
		response = requests.post(url=url, data=data)
		response = json.loads(response.content)
		if response['result']:
			return response
		else:
			message = response['message']
	except requests.exceptions.ConnectionError as e:
		logger.error(logger_format(e, api_ftp_account_create.func_name))
		message = _('Connection timed out')
	except requests.exceptions.RequestException as e:
		logger.error(logger_format(e, api_ftp_account_create.func_name))
		message = e
	except Exception as e:
		logger.error(logger_format(e, api_ftp_account_create.func_name))
		message = _('Could not connect to FTP server.')
	
	return {'result': False, 'data': [], 'message': message}


def api_ftp_account_delete(username, password):
	url = '{protocol}://{host}/account/delete'.format(
			protocol=settings.API_FTP_PROTOCOL,
			host=settings.API_FTP_HOST
	)
	
	data = {
		'username': username,
		'password': password
	}
	
	try:
		response = requests.post(url=url, data=data)
		response = json.loads(response.content)
		if response['result']:
			return response
		else:
			message = response['message']
	except requests.exceptions.ConnectionError as e:
		logger.error(logger_format(e, api_ftp_account_delete.func_name))
		message = _('Connection timed out')
	except requests.exceptions.RequestException as e:
		logger.error(logger_format(e, api_ftp_account_delete.func_name))
		message = e
	except Exception as e:
		logger.error(logger_format(e, api_ftp_account_delete.func_name))
		message = _('Could not connect to FTP server.')
	return {'result': False, 'data': [], 'message': message}
