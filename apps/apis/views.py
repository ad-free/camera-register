# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.translation import ugettext_lazy as _
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.firmware.models import Firmware
from ..cameras_token.models import EmbeddedCameraToken, Token
from ..brand.models import DeviceType, Brand
from ..cameras.models import Camera

from .utils import APIAccessPermission, CameraTokenPermission, camera_token_detail, publish_stream_generator
from ..commons.utils import logger_format, check_special_chars, optimize_request

from serializers import (
	CameraAuthenticateSerializer, CameraRegisterSerializer, CameraRequestSerializer,
	CameraConfigSerializer, CameraFirmwareDetailSerializer, CameraFirmwareUpgradeSerializer,
	CameraFirmwareDownloadSerializer
)

from ctypes import CDLL
from functools import partial

import logging
import time

logger = logging.getLogger('')


@swagger_auto_schema(methods=['post'], request_body=CameraAuthenticateSerializer)
@api_view(['POST'])
@permission_classes((partial(APIAccessPermission, 'api_camera_authenticate'),))
@transaction.atomic
def api_camera_authenticate(request):
	logger.info(logger_format('-------- START -------', api_camera_authenticate.func_name))
	errors = {}
	errors_code = 4
	serial = request.data.get('serial', '').strip()
	t = request.data.get('t', '').strip()
	tk = request.data.get('tk', '').strip()

	if not serial:
		errors.update({'message': _('This field is required.')})
	elif check_special_chars(serial) and len(serial) > 30:
		errors.update({'message': _('Incorrect formatting.')})
	if not t:
		errors.update({'message': _('This field is required.')})
	if not tk:
		errors.update({'message': _('This field is required.')})

	if not errors:
		try:
			fpt_hmac = CDLL(settings.LIB_IPC_HMAC_PATH)
			camera = Camera.objects.get(serial=serial)
			token = EmbeddedCameraToken.objects.get(camera=camera)
			data = fpt_hmac.FPTHmac_check(t, token.key, serial, tk)
			if data == 0:
				return Response({
					'serial': serial,
					'result': True
				}, status=status.HTTP_200_OK)
			errors_code = data
		except Camera.DoesNotExist:
			errors.update({'message': _('Camera does not exists.')})
			logger.info(logger_format('Camera does not exists.', api_camera_authenticate.func_name))
		except Exception as e:
			errors.update({'message': _('Server is error. Please try again later.')})
			logger.info(logger_format(e, api_camera_authenticate.func_name))

	logger.info(logger_format('-------- END -------', api_camera_authenticate.func_name))
	return Response({
		'serial': serial,
		'error_code': errors_code,
		'result': False
	}, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['post'], request_body=CameraRegisterSerializer)
@api_view(['POST'])
@permission_classes((partial(APIAccessPermission, 'api_camera_register'),))
@transaction.atomic
def api_camera_register(request):
	logger.info(logger_format('-------- START -------', api_camera_register.func_name))
	ctx = {}
	register = request.data.get('Register', '')

	if 'AuthCode' not in register:
		ctx.update({'AuthCode': _('This field is required.')})
		logger.error(logger_format('{}-{}'.format('AuthCode', 'This field is required.'), api_camera_register.func_name))
	elif not register['AuthCode']:
		ctx.update({'AuthCode': _('This field is required.')})
		logger.error(logger_format('{}-{}'.format('AuthCode', 'This field is required.'), api_camera_register.func_name))
	if 'ProductID' not in register:
		ctx.update({'ProductID': _('This field is required.')})
		logger.error(logger_format('{}-{}'.format('ProductID', 'This field is required.'), api_camera_register.func_name))
	elif not register['ProductID']:
		ctx.update({'ProductID': _('This field is required.')})
		logger.error(logger_format('{}-{}'.format('ProductID', 'This field is required.'), api_camera_register.func_name))
	if 'SerialNo' not in register:
		ctx.update({'SerialNo': _('This field is required.')})
		logger.error(logger_format('{}-{}'.format('SerialNo', 'This field is required.'), api_camera_register.func_name))
	elif not register['SerialNo']:
		ctx.update({'SerialNo': _('This field is required.')})
		logger.error(logger_format('{}-{}'.format('SerialNo', 'This field is required.'), api_camera_register.func_name))
	if 'FirmWare' not in register:
		ctx.update({'FirmWare': _('This field is required.')})
		logger.error(logger_format('{}-{}'.format('FirmWare', 'This field is required.'), api_camera_register.func_name))
	elif not register['FirmWare']:
		ctx.update({'FirmWare': _('This field is required.')})
		logger.info(logger_format('{}-{}'.format('FirmWare', 'This field is required.'), api_camera_register.func_name))

	if not ctx:
		try:
			camera = Camera.objects.get(serial=register['SerialNo'])
			camera.firmware = register['FirmWare']
			try:
				device_type = DeviceType.objects.get(code_number=register['ProductID'])
				brand = Brand.objects.get(devices_type=device_type)
				camera.device_type = device_type
				camera.brand = brand
			except DeviceType.DoesNotExist:
				camera.device_type = None
			except Brand.DoesNotExist:
				camera.brand = None
			camera.save()
			return Response({
				'Cmd': 'Register',
				'Register': {
					'AuthCodeRetry': settings.AUTH_CODE_RETRY,
					'ReAuthCodeServer': settings.RE_AUTH_CODE_SERVER
				},
				'Token': camera_token_detail(camera).get('token', ''),
				'Utc': int(time.time()),
				'Ret': status.HTTP_200_OK,
			}, status=status.HTTP_200_OK)
		except Camera.DoesNotExist:
			logger.error(logger_format('Camera does not exists.', api_camera_register.func_name))
		except Exception as e:
			logger.error(logger_format(e, api_camera_register.func_name))

	logger.info(logger_format('-------- END -------', api_camera_register.func_name))
	return Response({
		'Cmd': 'Register',
		'Utc': int(time.time()),
		'Ret': status.HTTP_100_CONTINUE
	}, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['post'], request_body=CameraRequestSerializer)
@api_view(['POST'])
@permission_classes((partial(APIAccessPermission, 'api_camera_request'), CameraTokenPermission))
def api_camera_request(request):
	logger.info(logger_format('-------- START -------', api_camera_request.func_name))
	ctx = {}
	serial = request.data.get('SerialNo', '')
	token = request.data.get('Token', '')

	logger.info(logger_format('Check serial', api_camera_request.func_name))
	if not serial:
		logger.error(logger_format('SerialNo is required.', api_camera_request.func_name))
		ctx.update({'SerialNo': _('This field is required.')})
	if not token:
		logger.error(logger_format('Token is required.', api_camera_request.func_name))
		ctx.update({'Token': _('This field is required.')})

	logger.info(logger_format('Check the parameters include Name, SerialNo', api_camera_request.func_name))
	if not ctx:
		try:
			camera = Camera.objects.get(serial=serial)
			EmbeddedCameraToken.objects.get(camera=camera, key=token)
			node = Token.objects.get(camera=camera)
			return Response({
				'Cmd': 'Request',
				'Token': token,
				'Utc': int(time.time()),
				'TimeUpdate': time.mktime(node.created_at.timetuple()),
				'Data': [
					{
						'Network.RTMP': {
							'Host': settings.WOWZA_SERVER,
							'Enable': settings.WOWZA_ALLOW_CONNECT_RTMP,
							'Port': settings.WOWZA_PORT[1],
							'Node': publish_stream_generator(serial, node.token)
						}
					}
				],
				'Ret': status.HTTP_200_OK
			}, status=status.HTTP_200_OK)
		except Camera.DoesNotExist:
			logger.error(logger_format('Camera does not exists.', api_camera_request.func_name))
		except EmbeddedCameraToken.DoesNotExist:
			logger.error(logger_format('Token does not exists.', api_camera_request.func_name))
		except Token.DoesNotExist:
			logger.error(logger_format('Publish stream does not exists.', api_camera_request.func_name))

	logger.info(logger_format('-------- END -------', api_camera_request.func_name))
	return Response({
		'Cmd': 'Request',
		'Token': request.META.get('HTTP_TOKEN', ''),
		'Utc': int(time.time()),
		'Ret': status.HTTP_100_CONTINUE
	}, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['post'], request_body=CameraConfigSerializer)
@api_view(['POST'])
@permission_classes((partial(APIAccessPermission, 'api_camera_config'), CameraTokenPermission))
def api_camera_config(request):
	logger.info(logger_format('-------- START -------', api_camera_config.func_name))
	ctx = {}
	serial = request.data.get('SerialNo', '')
	token = request.data.get('Token', '')

	logger.info(logger_format('Check serial', api_camera_config.func_name))
	if not serial:
		logger.error(logger_format('SerialNo is required.', api_camera_config.func_name))
		ctx.update({'SerialNo': _('This field is required.')})

	logger.info(logger_format('Check the parameters include Name, SerialNo', api_camera_config.func_name))
	if not ctx:
		try:
			camera = Camera.objects.get(serial=serial)
			EmbeddedCameraToken.objects.get(camera=camera, key=token)
			camera_topic = camera.camera_topic
			with open(camera_topic.ca_path.url[1:], 'r') as f:
				certificate = f.read()
			logger.info(logger_format('-------- END -------', api_camera_config.func_name))
			return Response({
				'Cmd': 'Get',
				'Token': request.META.get('HTTP_TOKEN', ''),
				'Utc': int(time.time()),
				'GetDefaultCfg': {
					'CfgServer': {
						'Mqtt': [
							{
								'Enable': settings.API_QUEUE_ENABLE,
								'Server': {
									'Host': camera.camera_topic.host if camera.camera_topic.host else '',
									'Port': camera.camera_topic.port if camera.camera_topic.port else '',
									'Protocol': 'mqtt',
									'TLSConfiguration': {
										'Enable': camera.camera_topic.ssl if camera.camera_topic.ssl else '',
										'TLSVersion': settings.API_QUEUE_TLS_VERSION[2],
										'CACertificate': certificate if certificate else ''
									},
									'Topics': {
										'Subscribe': {i.title(): j for i, j in camera_topic.topics.get('management', '').get('topics')['subscribe'].items()},
										'Publish': {i.title(): j for i, j in camera_topic.topics.get('management', '').get('topics')['publish'].items()}
									},
									'Account': {
										'Username': camera_topic.topics.get('management', '').get('account', '')['username'],
										'Password': camera_topic.topics.get('management', '').get('account', '')['password']
									}
								}
							}
						],
						'Http': {
							'Url': '{protocol}://{host}/api/v2/camera/request/'.format(
									protocol=settings.API_HOST_PROTOCOL,
									host=settings.API_HOST_RTMP
							),
							'Ssl': True if settings.API_HOST_PROTOCOL == 'https' else False,
							'Enable': settings.API_HOST_ENABLE,
							'RequestRetry': settings.AUTH_CODE_RETRY
						},
					},
					'IPCCfg': [
						{
							'ModifyUserPW': {
								'EncryptType': 'MD5',
								'NewPassWord': '6QNMIQGe',
								'PassWord': 'tlJwpbo6',
								'UserName': 'admin'
							}
						}
					]
				},
				'Ret': status.HTTP_200_OK
			}, status=status.HTTP_200_OK)
		except Camera.DoesNotExist:
			logger.error(logger_format('Camera does not exists.', api_camera_config.func_name))
		except EmbeddedCameraToken.DoesNotExist:
			logger.error(logger_format('Token does not exists.', api_camera_config.func_name))
		except ObjectDoesNotExist:
			logger.error(logger_format('No topics found.', api_camera_config.func_name))
		except Exception as e:
			logger.error(logger_format(e, api_camera_config.func_name))

	logger.info(logger_format('-------- END -------', api_camera_config.func_name))
	return Response({
		'Cmd': 'Get',
		'Name': 'GetDefaultCfg',
		'Token': request.META.get('HTTP_TOKEN', ''),
		'Utc': int(time.time()),
		'Ret': status.HTTP_100_CONTINUE
	}, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['post'], request_body=CameraFirmwareDetailSerializer)
@api_view(['POST'])
@permission_classes((partial(APIAccessPermission, 'api_camera_firmware_details'), CameraTokenPermission))
def api_camera_firmware_details(request):
	logger.info(logger_format('-------- START -------', api_camera_firmware_details.func_name))
	ctx = {}
	serial = request.data.get('SerialNo', '')
	token = request.data.get('Token', '')

	logger.info(logger_format('Check serial', api_camera_firmware_details.func_name))
	if not serial:
		ctx.update({'serial': _('This field is required')})
	elif len(serial) > 30 or not check_special_chars(serial):
		ctx.update({'serial': _('Incorrect formatting')})

	logger.info(logger_format('Check the parameters include serial and token', api_camera_firmware_details.func_name))
	if not ctx:
		try:
			camera = Camera.objects.get(serial=serial)
			EmbeddedCameraToken.objects.get(camera=camera, key=token)
			obj_firmware = Firmware.objects.filter(type__code_number=camera.device_type.code_number).latest('created_at')
			return Response({
				'Cmd': 'Get',
				'Token': token,
				'Utc': int(time.time()),
				'FirmwareInfo': {
					'ProductID': camera.device_type.code_number,
					'Firmware': obj_firmware.version,
					'Url': '{protocol}://{host}/api/v2/camera/firmware/download/'.format(
							protocol=settings.API_HOST_PROTOCOL,
							host=settings.API_HOST_DEFAULT
					)
				},
				'Ret': status.HTTP_200_OK
			}, status=status.HTTP_200_OK)
		except Camera.DoesNotExist:
			logger.error(logger_format('Camera does not exists', api_camera_firmware_details.func_name))
		except EmbeddedCameraToken.DoesNotExist:
			logger.error(logger_format('Token does not exists', api_camera_firmware_details.func_name))
		except Firmware.DoesNotExist:
			return Response({
				'Cmd': 'Get',
				'Token': token,
				'Utc': int(time.time()),
				'Name': 'FirmwareInfo',
				'Ret': status.HTTP_200_OK
			}, status=status.HTTP_200_OK)
		except Exception as e:
			logger.error(logger_format(e, api_camera_firmware_details.func_name))

	return Response({
		'Cmd': 'Get',
		'Token': token,
		'Utc': int(time.time()),
		'Name': 'FirmwareInfo',
		'Ret': status.HTTP_100_CONTINUE
	}, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['post'], request_body=CameraFirmwareUpgradeSerializer)
@api_view(['POST'])
@permission_classes((partial(APIAccessPermission, 'api_camera_firmware_upgrade'),))
@transaction.atomic
def api_camera_firmware_upgrade(request):
	logger.info(logger_format('-------- START -------', api_camera_firmware_upgrade.func_name))
	ctx = {}
	firmware_file = ''
	serial = optimize_request(request.data.get('serial', ''))
	firmware_version = optimize_request(request.data.get('firmware_version', ''))

	logger.info(logger_format('Check serial', api_camera_firmware_upgrade.func_name))
	if not serial:
		ctx.update({'serial': _('This field is required')})
	elif len(serial) > 30 or not check_special_chars(serial):
		ctx.update({'serial': _('Incorrect formatting')})

	logger.info(logger_format('Firmware version is empty', api_camera_firmware_upgrade.func_name))
	if not firmware_version:
		ctx.update({'firmware_version': _('This field is required')})

	try:
		firmware_file = request.FILES['firmware_file']
	except MultiValueDictKeyError:
		logger.error(logger_format('Firmware is empty', api_camera_firmware_upgrade.func_name))
		ctx.update({'firmware_file': _('This field is required')})

	logger.info(logger_format('Check the parameters include serial, firmware_name, firmware_version', api_camera_firmware_upgrade.func_name))
	if not ctx:
		try:
			camera = Camera.objects.get(serial=serial)
		except Camera.DoesNotExist:
			logger.error(logger_format('Camera does not exists', api_camera_firmware_upgrade.func_name))
			ctx.update({'message': _('Camera does not exists')})
		else:
			camera.firmware.release_file = firmware_file
			camera.firmware.save()
			fs = FileSystemStorage()
			filename = fs.save(settings.MEDIA_ROOT + '/firmware/' + camera.serial + '.json', firmware_file)
			logger.info(logger_format('-------- END -------', 'api_camera_firmware'))
			return Response({
				'status': status.HTTP_200_OK,
				'result': True,
				'data': filename
			}, status=status.HTTP_200_OK)

	logger.info(logger_format('-------- END -------', 'api_camera_firmware'))
	return Response({
		'status': status.HTTP_400_BAD_REQUEST,
		'result': False,
		'errors': {'message': _('Error, please try again later')} if not ctx else ctx
	}, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['post'], request_body=CameraFirmwareDownloadSerializer)
@api_view(['POST'])
@permission_classes((partial(APIAccessPermission, 'api_camera_firmware_download'), CameraTokenPermission))
def api_camera_firmware_download(request):
	logger.info(logger_format('-------- START -------', api_camera_firmware_download.func_name))
	ctx = {}
	serial = request.data.get('SerialNo', '')
	token = request.data.get('Token', '')

	logger.info(logger_format('Check serial', api_camera_firmware_download.func_name))
	if not serial:
		ctx.update({'SerialNo': _('This field is required.')})
		logger.info(logger_format('SerialNo is required.', api_camera_firmware_download.func_name))
	elif len(serial) > 30 or not check_special_chars(serial):
		ctx.update({'SerialNo': _('Incorrect formatting.')})
		logger.info(logger_format('SerialNo incorrect formatting.', api_camera_firmware_download.func_name))

	if not token:
		ctx.update({'Token': _('This field is required.')})
		logger.info(logger_format('Token is required.', api_camera_firmware_download.func_name))

	logger.info(logger_format('Check the parameters include serial, firmware_name, firmware_version', api_camera_firmware_download.func_name))
	if not ctx:
		try:
			camera = Camera.objects.get(serial=serial)
			EmbeddedCameraToken.objects.get(camera=camera, key=token)
			firmware = Firmware.objects.filter(type=camera.device_type).latest('created_at')
			response = HttpResponse(firmware.release_file, content_type='application/zip')
			response['Content-Disposition'] = 'attachment; filename=%s' % firmware.version
			return response
		except Camera.DoesNotExist:
			logger.error(logger_format('Camera does not exists', api_camera_firmware_download.func_name))
		except Exception as e:
			logger.error(logger_format(e, api_camera_firmware_download.func_name))

	logger.info(logger_format('-------- END -------', api_camera_firmware_download.func_name))
	return Response({
		'Cmd': 'Get',
		'Token': request.META.get('HTTP_TOKEN', ''),
		'Utc': int(time.time()),
		'Name': 'DownloadFirmWare',
		'Ret': status.HTTP_100_CONTINUE
	}, status=status.HTTP_200_OK)
