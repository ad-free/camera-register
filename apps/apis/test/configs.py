API_MANAGEMENT_PROTOCOL = 'https'
API_MANAGEMENT_HOST = 'prod-management.iotc.vn'
API_MANAGEMENT_PROTOCOL_LOCAL = 'http'
API_MANAGEMENT_HOST_LOCAL = '192.168.2.132'
API_MANAGEMENT_PORT_LOCAL = 8000
API_MANAGEMENT_GIS = 'd0241d2e185f4cd5a1d53d21c0ef8df2'
API_MANAGEMENT_LOCAL = False

API_MANAGEMENT_LIST = {
	'sign-in': '{protocol}://{host}/api/v2/auth/sign-in/',
	'sign-out': '{protocol}://{host}/api/v2/auth/sign-out/',
	'camera-register': '{protocol}://{host}/api/v2/camera/register/',
	'camera-request': '{protocol}://{host}/api/v2/camera/request/',
	'camera-config': '{protocol}://{host}/api/v2/camera/config/',
	'firmware-upgrade': '{protocol}://{host}/api/v2/camera/firmware/upgrade/',
	'firmware-download': '{protocol}://{host}/api/v2/camera/firmware/download/',
	'firmware-details': '{protocol}://{host}/api/v2/camera/firmware/details/',
	'camera-add': '{protocol}://{host}/api/v2/camera/add/',
	'camera-delete': '{protocol}://{host}/api/v2/camera/delete/',
	'camera-publish-stream': '{protocol}://{host}/api/v2/camera/create/publish-stream/',
	'camera-stream-name': '{protocol}://{host}/api/v2/camera/create/stream-name/',
	'firmware-version': '{protocol}://{host}/api/v2/camera/firmware/version/',
	'config-update': '{protocol}://{host}/api/v2/camera/config/update/',
	'config-list': '{protocol}://{host}/api/v2/camera/config/list/',
	'server-update': '{protocol}://{host}/api/v2/server/update/',
}

API_MANAGEMENT_LIST_LOCAL = {
	'sign-in': '{protocol}://{host}:{port}/api/v2/auth/sign-in/',
	'sign-out': '{protocol}://{host}:{port}/api/v2/auth/sign-out/',
	'camera-register': '{protocol}://{host}:{port}/api/v2/camera/register/',
	'camera-request': '{protocol}://{host}:{port}/api/v2/camera/request/',
	'camera-config': '{protocol}://{host}:{port}/api/v2/camera/config/',
	'firmware-upgrade': '{protocol}://{host}:{port}/api/v2/camera/firmware/upgrade/',
	'firmware-download': '{protocol}://{host}:{port}/api/v2/camera/firmware/download/',
	'firmware-details': '{protocol}://{host}:{port}/api/v2/camera/firmware/details/',
	'camera-add': '{protocol}://{host}:{port}/api/v2/camera/add/',
	'camera-delete': '{protocol}://{host}:{port}/api/v2/camera/delete/',
	'camera-publish-stream': '{protocol}://{host}:{port}/api/v2/camera/create/publish-stream/',
	'camera-stream-name': '{protocol}://{host}:{port}/api/v2/camera/create/stream-name/',
	'firmware-version': '{protocol}://{host}:{port}/api/v2/camera/firmware/version/',
	'config-update': '{protocol}://{host}:{port}/api/v2/camera/config/update/',
	'config-list': '{protocol}://{host}:{port}/api/v2/camera/config/list/',
	'server-update': '{protocol}://{host}:{port}/api/v2/server/update/',
}
