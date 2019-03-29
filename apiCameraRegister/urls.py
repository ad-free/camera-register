"""apiCameraRegister URL Configuration"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
	url(r'^', admin.site.urls),
	url(r'^api/v2/', include('apps.apis.urls')),
]

admin.site.site_header = 'Management - System Administration'
admin.site.index_title = 'FPT Management System'
admin.site.site_title = 'FPT'

if 'django_prometheus' in settings.INSTALLED_APPS:
	urlpatterns += [url(r'^', include('django_prometheus.urls'))]
