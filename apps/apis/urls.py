# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.apis import views

docs = get_schema_view(
		openapi.Info(
				title='Snippets API',
				default_version='v1.0',
				description='',
				terms_of_service='',
				contact=openapi.Contact(email='duyta8@fpt.com.vn')
		),
		public=True,
		permission_classes=(permissions.IsAuthenticated,),
)

re_doc = get_schema_view(
		openapi.Info(
				title='Snippets API',
				default_version='v1.0',
				description='',
				terms_of_service='',
				contact=openapi.Contact(email='duyta8@fpt.com.vn')
		),
		public=True,
		permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
)

urlpatterns = [
	# Docs
	url(r'^docs/$', login_required(docs.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
	url(r'^redoc/$', login_required(re_doc.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
	# Flow camera get config
	url(r'^camera/register/$', views.api_camera_register, name='api_camera_register'),
	url(r'^camera/request/$', views.api_camera_request, name='api_camera_request'),
	url(r'^camera/config/$', views.api_camera_config, name='api_camera_config'),
	url(r'^camera/firmware/upgrade/$', views.api_camera_firmware_upgrade, name='api_camera_firmware_upgrade'),
	url(r'^camera/firmware/download/$', views.api_camera_firmware_download, name='api_camera_firmware_download'),
	url(r'^camera/firmware/details/$', views.api_camera_firmware_details, name='api_camera_firmware_details'),
	url(r'^camera/authenticate/$', views.api_camera_authenticate, name='api_camera_authenticate'),
]
