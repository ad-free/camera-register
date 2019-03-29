# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


@login_required
def get_qr_code(request, product_code, template='qr-code/qr_code.html'):
	if request.user.is_staff:
		return render(request, template, context={'product_code': product_code})
	raise PermissionDenied
