# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Staff


@admin.register(Staff)
class StaffAdmin(UserAdmin):
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
	)
	list_display = ('username', 'first_name', 'last_name', 'email', 'is_active', 'last_login')
	list_filter = ['is_active', 'date_joined', 'last_login']
	exclude = ('user_permissions',)
