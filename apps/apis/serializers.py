# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers


class CameraAuthenticateSerializer(serializers.Serializer):
	serial = serializers.CharField(max_length=32, required=True)
	t = serializers.CharField(max_length=100, required=True)
	tk = serializers.CharField(max_length=255, required=True)

	def create(self, validated_data):
		pass

	def update(self, instance, validated_data):
		pass


class CameraRegisterSerializer(serializers.Serializer):
	Register = serializers.JSONField(required=True)

	def create(self, validated_data):
		pass

	def update(self, instance, validated_data):
		pass


class CameraRequestSerializer(serializers.Serializer):
	SerialNo = serializers.CharField(max_length=32, required=True)
	Token = serializers.CharField(max_length=255, required=True)

	def create(self, validated_data):
		pass

	def update(self, instance, validated_data):
		pass


class CameraConfigSerializer(serializers.Serializer):
	SerialNo = serializers.CharField(max_length=32, required=True)
	Token = serializers.CharField(max_length=255, required=True)

	def create(self, validated_data):
		pass

	def update(self, instance, validated_data):
		pass


class CameraFirmwareDetailSerializer(serializers.Serializer):
	SerialNo = serializers.CharField(max_length=32, required=True)
	Token = serializers.CharField(max_length=255, required=True)

	def create(self, validated_data):
		pass

	def update(self, instance, validated_data):
		pass


class CameraFirmwareUpgradeSerializer(serializers.Serializer):
	serial = serializers.CharField(max_length=32, required=True)
	firmware_version = serializers.CharField(max_length=100, required=True)

	def create(self, validated_data):
		pass

	def update(self, instance, validated_data):
		pass


class CameraFirmwareDownloadSerializer(serializers.Serializer):
	SerialNo = serializers.CharField(max_length=32, required=True)
	Token = serializers.CharField(max_length=255, required=True)

	def create(self, validated_data):
		pass

	def update(self, instance, validated_data):
		pass
