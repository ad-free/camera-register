# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils.dateformat import format
from django.utils.translation import ugettext_lazy as _

from .models import Registration

from rest_framework import permissions

from ..apis.aes import AESCipher
from ..cameras_token.models import EmbeddedCameraToken

from datetime import datetime, timedelta
from Crypto.Hash import SHA256, MD5

import logging
import pytz

logger = logging.getLogger('')


def publish_stream_generator(serial, message):
	m = MD5.new(data=serial)
	token = AESCipher(key=m.hexdigest()).decrypt(message)
	if token:
		return token
	return ''


def automatically_create_stream_names(serial, message):
	m = MD5.new(data=serial)
	token = AESCipher(key=m.hexdigest()).decrypt(message).split('-')[settings.TOKEN_SECRET_KEY_POSITION]
	d = datetime.now(pytz.timezone(settings.TIME_ZONE))
	key = SHA256.new(data=token)
	stream_name = AESCipher(key=key.digest(), salt=settings.TOKEN_IV).encrypt(d.strftime('%d:%m:%Y:%H:%M:%S'))
	if '/' in stream_name:
		stream_name = stream_name.replace('/', settings.TOKEN_SECRET_KEY_SPECIAL_CHARACTER)
	return '{protocol}://{server}:{port}/{application}/_definst_/{stream_name}'.format(
			protocol=settings.STREAM_PROTOCOL[0],
			server=settings.WOWZA_SERVER,
			port=settings.WOWZA_PORT[1],
			application=serial,
			stream_name=stream_name
	)


def app_registration(app_id):
	app = Registration.objects.distinct().filter(app_id=app_id, status=True).prefetch_related('features').last()
	if app:
		features = list(app.features.values_list('name', flat=True))
		return {
			'app_package': app.app_package,
			'app_type': app.app_type,
			'server_status': app.server,
			'features': features
		}
	return None


def file_camera_package_update(camera, serial, package_type):
	service_file = open(settings.MEDIA_DIR + '/packages/' + str(camera.ftp_camera.all().first().server) + '.usedservice', 'w+')
	content = service_file.read()
	position_serial = content.find('{}:'.format(serial))
	if position_serial != -1 and content[position_serial + len(serial)] == ':':
		content_list = list(content)
		content_list[position_serial + len(serial) + 1: position_serial + len(serial) + 3] = list('%02d' % int(package_type))
		content = ''.join(content_list)
		service_file.seek(0)
		service_file.truncate()
		service_file.write(str(content))
	else:
		service_file.close()
		a_file = open(settings.MEDIA_DIR + '/packages/' + str(camera.ftp_camera.all().first().server) + '.usedservice', 'a+')
		line = '%s%s:%02d' % ('\n' if content else '', serial, int(package_type))
		a_file.write(str(line))
		a_file.close()
	service_file.close()


def camera_token_detail(camera):
	obj_key = {'token': ''}
	try:
		obj_token = EmbeddedCameraToken.objects.get(camera=camera)
		obj_key['token'] = obj_token.key
	except EmbeddedCameraToken.DoesNotExist:
		obj_token = EmbeddedCameraToken.objects.create(camera=camera)
		obj_key['token'] = obj_token.key
	except Exception as e:
		logger.error('{}'.format(e))
		pass
	return obj_key


class APIAccessPermission(permissions.BasePermission):
	message = _('Page was not found on this server.')

	def __init__(self, stack):
		self.stack = stack

	def has_permission(self, request, view):
		try:
			if 'HTTP_GIS' in request.META:
				app_id = request.META.get('HTTP_GIS', '')
				if len(app_id) > 0:
					if request.session.get(app_id, None) is None:
						app = app_registration(app_id)
						app.update({'session_created': int(format(datetime.now(), u'U'))})
						request.session[app_id] = app
					else:
						temp = request.session[app_id]
						time_ago = int(format(datetime.now() - timedelta(seconds=180), u'U'))
						if time_ago > int(temp['session_created']):
							app = app_registration(app_id)
							app.update({'session_created': int(format(datetime.now(), u'U'))})
							request.session[app_id] = app
						else:
							app = request.session[app_id]
					# Checking permission to access APIs
					if app:
						if app['app_type'] == 'web':
							if request.META['HTTP_HOST'] not in app['app_package']:
								return False
						else:
							if 'HTTP_PACKAGE' not in request.META:
								return False
							elif request.META['HTTP_PACKAGE'] not in app['app_package']:
								return False
						app_feature = self.stack
						if app_feature in app['features']:
							return True
		except Exception as e:
			logger.error('{}'.format(e))
			pass
		return False


class CameraTokenPermission(permissions.BasePermission):
	message = _('Token invalid.')

	def has_permission(self, request, view):
		try:
			if 'HTTP_TOKEN' in request.META:
				token = request.META.get('HTTP_TOKEN', '')
				if len(token) > 0:
					try:
						EmbeddedCameraToken.objects.get(key=token)
					except EmbeddedCameraToken.DoesNotExist:
						pass
					else:
						return True
		except Exception as e:
			logger.error('{}'.format(e))
			pass
		return False
