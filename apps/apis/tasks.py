from .apis import api_queue_sign_up, api_wowza_delete_application
import threading


def threading_functions(function_list, is_waiting=True):
	threads = []
	for (function_name, function_args) in function_list:
		t = threading.Thread(target=function_name, args=function_args)
		t.start()
		threads.append(t)
	if is_waiting:
		for thread in threads:
			thread.join()
	return


def task_api_queue_sign_up(username, password, is_system, que):
	response = api_queue_sign_up(username, password, is_system)
	que.put(response)


def task_api_wowza_delete_application(serial, queue):
	response = api_wowza_delete_application(serial)
	queue.put(response)
