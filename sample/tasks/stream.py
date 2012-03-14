from celery.contrib.abortable import Task
from celery.registry import tasks
from sample.scripts.stream import StreamManage
from pprint import pprint

class StreamTask(Task):
	
	sm = None #StreamManager class instance
	th = None #Threading class instace
	action = None
	
	def __init__(self):
		pass
		
	def run(self, coords, **kwargs):
		try:
			# This is not debug is required to check keys on 'stop'
			self.action = coords['stop']
			print "StreamTask ::: command from client is::: %s" % coords['stop']
			try:
				self.th = self.sm.stream(coords, obj = self.th)
			except AttributeError, e:
				print "StreamTask ::: no Threading instance retry %s" % e
				self.retry(args = [coords], exc=e, countdown=5, kwargs=kwargs)
		except KeyError, e:				
			print "StreamTask ::: Stream instantiated, for exception %s" % e
			self.sm = StreamManage(coords['bounds_id'])
			self.th = self.sm.stream(coords)
		print "From sample.task  Task is %s" % self.request.id + " the returned result from script called is %s" % self.th + " instance of StreamingManager class is %s" % self.sm
		return 'task executed'
		
tasks.register(StreamTask)