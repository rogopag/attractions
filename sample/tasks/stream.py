from celery.task import Task
from celery.registry import tasks
from sample.scripts.stream import stream
from pprint import pprint

class StreamTask(Task):
	def run(self, coords, **kwargs):
		r = stream(coords)
		return r
		
tasks.register(StreamTask)