from celery.contrib.abortable import AbortableTask
from celery.registry import tasks
from sample.scripts.stream import StreamManage
from celery.task.control import revoke
from pprint import pprint

class StreamTask(AbortableTask):
	def run(self, coords, **kwargs):
		sm = StreamManage()
		r = sm.stream(coords)
		print "From sample.task  Task is %s" % self.request.id + " the returned result from script called is %s" % r
		return r
		
tasks.register(StreamTask)