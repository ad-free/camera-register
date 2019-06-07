# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import Account


class AccountForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(), required=False)
	old_password = forms.CharField(widget=forms.PasswordInput(), required=False)

	class Meta:
		model = Account
		fields = '__all__'
