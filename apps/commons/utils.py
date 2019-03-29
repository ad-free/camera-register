# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import re
import string

from Crypto.Hash import MD5, SHA256
from django.conf import settings

from ..apis.aes import AESCipher


def decrypt_stream_name(stream_name, token):
	key = SHA256.new(data=token)
	return AESCipher(key=bytes(key.digest()), salt=settings.TOKEN_IV).decrypt(stream_name)


def encrypt_password(message, secret=''):
	if not secret:
		key = MD5.new(data=message).hexdigest()
	else:
		key = secret
	return AESCipher(key).encrypt(message)


def decrypt_password(message, code=''):
	if not code:
		key = MD5.new(data=code).hexdigest()
	else:
		key = code
	return AESCipher(key).decrypt(message)


def token_key_generator(serial, length=8, circle=10):
	tmp = ''
	chars = string.ascii_letters + string.digits
	for i in range(circle):
		tmp += ''.join(random.sample(chars, length)) + '-'
	m = MD5.new(data=serial)
	return {
		'message': tmp.rstrip('-'),
		'token': AESCipher(key=m.hexdigest()).encrypt(tmp.rstrip('-'))
	}


def remove_special_chars(char):
	return char.strip().translate({ord(c): '' for c in '!@#$%^&*()[]{};:,./<>?\|`~-=_+"'})


def check_special_chars(char, is_product_code=False):
	regex = "^[a-zA-Z0-9]*$" if is_product_code else "^[a-z0-9]*$"
	if re.match(regex, char):
		return True
	return False


def optimize_request(content):
	if content is not None:
		string_convert = unicode(repr(content), 'unicode-escape')
		if string_convert.startswith('u'):
			return string_convert[2:-1].strip()
		return string_convert.strip()
	return None


def logger_format(message, func_name):
	log_format = {
		'message': message,
		'func_name': func_name
	}
	return log_format

