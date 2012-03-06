from celery.task import Task
from celery.registry import tasks
from sample.scripts.stream import StreamManage
from pprint import pprint

class StreamTask(Task):
	def run(self, coords, **kwargs):
		sm = StreamManage()
		r = sm.stream(coords)
		return r
		
tasks.register(StreamTask)